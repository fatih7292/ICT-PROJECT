#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IM-3. Исследование связи промышленного энергопотребления и режимов работы
=========================================================================
Набор данных : Hyrasiaone_green_hydrogen_plant_data.csv
               (35 040 интервалов по 15 минут, 2018 г.; Usage_kWh — энергия за интервал).

Этапы (соответствуют разделу IV задания)
----------------------------------------
 1. Аудит данных: типы, пропуски, дубликаты, регулярность шага, единицы измерения.
    Исключение CO2(tCO2) (утечка целевой переменной). Временные признаки.
 2. Проверка гипотез (тест Уэлча, p-value, Cohen's d, 95% ДИ):
       H1: Usage_kWh при Maximum_Load  >  Usage_kWh при Light_Load       (односторонний)
       H2: Usage_kWh отличается при Temperature_C > медианы vs <= медианы (двусторонний)
 3. Многофакторная OLS (statsmodels), разбиение по времени 80/20.
    Метрики R², MAE, RMSE (на тесте), VIF, Durbin-Watson, Jarque-Bera, HAC-ошибки.
 4. Единая панель из 6 графиков (300 DPI) + текстовые пояснения.
 5. Проверка устойчивости: OLS на винсоризованных данных (1% с каждого края).
 6. Сценарий: перенос 10% пиковой нагрузки в средний режим при цене $0.10/кВт·ч.
 7. Три практические рекомендации (числа подставляются из расчётов).

Запуск
------
    python im3_energy_analysis.py --data "Hyrasiaone green hydrogen plant data.csv" --out results

Зависимости: numpy, pandas, scipy, matplotlib, seaborn, statsmodels
    pip install numpy pandas scipy matplotlib seaborn statsmodels
"""
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # без GUI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
from scipy.stats import gaussian_kde
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera

warnings.filterwarnings("ignore", category=FutureWarning)

# --------------------------------------------------------------------------- #
# 0. ПАРАМЕТРЫ ИССЛЕДОВАНИЯ
# --------------------------------------------------------------------------- #
SEED = 42                  # для bootstrap
TRAIN_FRAC = 0.80          # доля обучающей выборки (по времени)
WINSOR_P = 0.01            # доля усечения с КАЖДОГО края
PRICE_USD_PER_KWH = 0.10   # цена энергии
SHIFT_SHARE = 0.10         # доля пиковой нагрузки
HAC_MAXLAGS = 96           # 1 сутки (окно Ньюи-Уэста)
DPI = 300

TARGET = "Usage_kWh"
LOAD_ORDER = ["Light_Load", "Medium_Load", "Maximum_Load"]
LOAD_COLORS = {"Light_Load": "#4C9F70", "Medium_Load": "#E0A030", "Maximum_Load": "#C0392B"}

FEATURES_FULL = [
    "Temperature_C",
    "Lagging_Current_Reactive_Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor",
    "hour_sin", "hour_cos", "month_sin", "month_cos", "is_weekend",
]
FEATURES_CALENDAR = ["Temperature_C", "hour_sin", "hour_cos", "month_sin", "month_cos", "is_weekend"]
WINSOR_COLS = [TARGET, "Temperature_C",
               "Lagging_Current_Reactive_Power_kVarh", "Leading_Current_Reactive_Power_kVarh",
               "Lagging_Current_Power_Factor", "Leading_Current_Power_Factor"]

_LOG: list[str] = []

def log(msg: str = "") -> None:
    print(msg)
    _LOG.append(str(msg))

def hdr(title: str) -> None:
    log("\n" + "=" * 78 + f"\n{title}\n" + "=" * 78)

def fmt_p(p: float) -> str:
    return "< 1e-16" if p < 1e-16 else f"{p:.4g}"

# --------------------------------------------------------------------------- #
# 1. ЗАГРУЗКА И АУДИТ
# --------------------------------------------------------------------------- #
def load_and_audit(path: Path) -> tuple[pd.DataFrame, dict]:
    hdr("1. АУДИТ ДАННЫХ")
    df = pd.read_csv(path)
    audit: dict = {"rows": int(len(df)), "cols": int(df.shape[1])}
    log(f"Размер: {df.shape[0]} строк x {df.shape[1]} столбцов")

    # Время
    df["datetime"] = pd.to_datetime(df["datetime"])
    date_alt = pd.to_datetime(df["date"], format="%d/%m/%Y %H:%M")
    audit["date_equals_datetime"] = bool((date_alt == df["datetime"]).all())
    log(f"Столбцы 'date' и 'datetime' совпадают: {audit['date_equals_datetime']}")

    audit["dup_full_rows"] = int(df.duplicated().sum())
    audit["dup_timestamps"] = int(df["datetime"].duplicated().sum())
    log(f"Полные дубликаты строк: {audit['dup_full_rows']}; дубликаты времени: {audit['dup_timestamps']}")

    df = df.sort_values("datetime").reset_index(drop=True)
    steps = df["datetime"].diff().dropna().value_counts()
    audit["regular_15min"] = bool(len(steps) == 1 and steps.index[0] == pd.Timedelta(minutes=15))
    log(f"Период: {df['datetime'].min()} .. {df['datetime'].max()}; шаг строго 15 мин: {audit['regular_15min']}")

    # Утечка
    co2 = "CO2(tCO2)"
    r_co2 = df[[TARGET, co2]].corr().iloc[0, 1]
    audit["corr_usage_co2"] = float(r_co2)
    log(f"УТЕЧКА: corr({TARGET}, {co2}) = {r_co2:.4f} => столбец исключён.")
    df = df.drop(columns=[co2])

    # Признаки
    dt = df["datetime"].dt
    df["hour"] = dt.hour
    df["month"] = dt.month
    df["dayofweek"] = dt.dayofweek
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)
    hour_frac = dt.hour + dt.minute / 60.0
    df["hour_sin"] = np.sin(2 * np.pi * hour_frac / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hour_frac / 24)
    df["month_sin"] = np.sin(2 * np.pi * (df["month"] - 1) / 12)
    df["month_cos"] = np.cos(2 * np.pi * (df["month"] - 1) / 12)

    desc = df[[TARGET, "Temperature_C", "Lagging_Current_Reactive_Power_kVarh",
               "Leading_Current_Reactive_Power_kVarh", "Lagging_Current_Power_Factor",
               "Leading_Current_Power_Factor"]].describe().T
    desc["skew"] = df[desc.index].skew()
    audit["describe"] = desc
    return df, audit

# --------------------------------------------------------------------------- #
# 2. ПРОВЕРКА ГИПОТЕЗ
# --------------------------------------------------------------------------- #
def welch_test(a, b, alternative: str = "two-sided", ci_level: float = 0.95) -> dict:
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    m1, m2, v1, v2 = a.mean(), b.mean(), a.var(ddof=1), b.var(ddof=1)
    diff = m1 - m2
    se = np.sqrt(v1 / n1 + v2 / n2)
    t = diff / se
    df_w = (v1 / n1 + v2 / n2) ** 2 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    if alternative == "two-sided":
        p = 2 * stats.t.sf(abs(t), df_w)
    elif alternative == "greater":
        p = stats.t.sf(t, df_w)
    else:
        p = stats.t.cdf(t, df_w)
    tcrit = stats.t.ppf(1 - (1 - ci_level) / 2, df_w)
    sp = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    d = diff / sp
    se_d = np.sqrt((n1 + n2) / (n1 * n2) + d ** 2 / (2 * (n1 + n2)))
    return dict(n1=n1, n2=n2, mean1=m1, mean2=m2, sd1=np.sqrt(v1), sd2=np.sqrt(v2), diff=diff,
                t=t, df=df_w, p=p, ci_low=diff - tcrit * se, ci_high=diff + tcrit * se,
                d=d, d_ci_low=d - 1.96 * se_d, d_ci_high=d + 1.96 * se_d)

def interpret_d(d: float) -> str:
    ad = abs(d)
    return "ничтожный" if ad < 0.2 else "малый" if ad < 0.5 else "средний" if ad < 0.8 else "большой"

def print_test(name: str, r: dict, alt_label: str) -> None:
    log(f"\n{name} [{alt_label}]")
    log(f"  n1={r['n1']}, n2={r['n2']}; среднее1={r['mean1']:.3f}, среднее2={r['mean2']:.3f}; разность={r['diff']:.3f} кВт·ч")
    log(f"  t(Уэлч) = {r['t']:.3f}, df = {r['df']:.1f}, p = {fmt_p(r['p'])}")
    log(f"  95% ДИ разности средних: [{r['ci_low']:.3f}; {r['ci_high']:.3f}]")
    log(f"  Cohen's d = {r['d']:.3f} (95% ДИ [{r['d_ci_low']:.3f}; {r['d_ci_high']:.3f}]) — {interpret_d(r['d'])} эффект")

def run_hypotheses(df: pd.DataFrame) -> dict:
    hdr("2. ПРОВЕРКА ГИПОТЕЗ (тест Уэлча, alpha = 0.05)")
    out: dict = {}
    mx = df.loc[df["Load_Type"] == "Maximum_Load", TARGET]
    lt = df.loc[df["Load_Type"] == "Light_Load", TARGET]
    h1 = welch_test(mx, lt, alternative="greater")
    mw = stats.mannwhitneyu(mx, lt, alternative="greater")
    print_test("H1: Usage_kWh(Maximum) > Usage_kWh(Light)", h1, "односторонний")
    log(f"  Тест Манна-Уитни: p = {fmt_p(mw.pvalue)}")
    out["H1"] = {**h1, "mannwhitney_p": float(mw.pvalue)}

    med = df["Temperature_C"].median()
    hi = df.loc[df["Temperature_C"] > med, TARGET]
    lo = df.loc[df["Temperature_C"] <= med, TARGET]
    h2 = welch_test(hi, lo, alternative="two-sided")
    log(f"\nМедиана температуры = {med:.2f} °C")
    print_test("H2: Usage_kWh(T > med) vs Usage_kWh(T <= med)", h2, "двусторонний")
    mw2 = stats.mannwhitneyu(hi, lo, alternative="two-sided")
    log(f"  Тест Манна-Уитни: p = {fmt_p(mw2.pvalue)}")

    daily = df.set_index("datetime").resample("D").agg({TARGET: "mean", "Temperature_C": "mean"})
    dmed = daily["Temperature_C"].median()
    h2d = welch_test(daily.loc[daily["Temperature_C"] > dmed, TARGET], daily.loc[daily["Temperature_C"] <= dmed, TARGET])
    print_test("H2 (контроль, средние за сутки; автокорреляция исключена)", h2d, "двусторонний")
    out["H2"] = {**h2, "median_T": float(med), "mannwhitney_p": float(mw2.pvalue), "d": h2["d"]}
    out["H2_daily"] = h2d
    return out

# --------------------------------------------------------------------------- #
# 3. РЕГРЕССИЯ И ДИАГНОСТИКА
# --------------------------------------------------------------------------- #
def time_split(df: pd.DataFrame, frac: float = TRAIN_FRAC) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.sort_values("datetime").reset_index(drop=True)
    k = int(len(df) * frac)
    return df.iloc[:k].copy(), df.iloc[k:].copy()

def regression_metrics(y_true, y_pred) -> dict:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    e = y_true - y_pred
    return dict(R2=1 - np.sum(e ** 2) / np.sum((y_true - y_true.mean()) ** 2),
                MAE=np.mean(np.abs(e)), RMSE=np.sqrt(np.mean(e ** 2)))

def winsor_bounds(train: pd.DataFrame, cols: list[str], p: float = WINSOR_P) -> dict:
    return {c: (train[c].quantile(p), train[c].quantile(1 - p)) for c in cols}

def apply_winsor(d: pd.DataFrame, bounds: dict, cols: list[str]) -> pd.DataFrame:
    d = d.copy()
    for c in cols:
        d[c] = d[c].clip(*bounds[c])
    return d

def fit_ols(train: pd.DataFrame, test: pd.DataFrame, features: list[str], y_test_override: np.ndarray | None = None) -> dict:
    Xtr = sm.add_constant(train[features], has_constant="add")
    Xte = sm.add_constant(test[features], has_constant="add")
    res = sm.OLS(train[TARGET].values, Xtr).fit()
    res_hac = sm.OLS(train[TARGET].values, Xtr).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    pred_te = np.asarray(res.predict(Xte))
    y_te = test[TARGET].values if y_test_override is None else y_test_override
    return dict(features=features, res=res, res_hac=res_hac, Xtr=Xtr, pred_test=pred_te,
                resid_test=y_te - pred_te, y_test=y_te,
                metrics_test=regression_metrics(y_te, pred_te),
                metrics_train=regression_metrics(train[TARGET].values, np.asarray(res.fittedvalues)))

def run_regression(df: pd.DataFrame) -> dict:
    hdr("3. РЕГРЕССИЯ OLS И ДИАГНОСТИКА")
    train, test = time_split(df)
    log(f"Train: {len(train)} набл., Test: {len(test)} набл.")

    full = fit_ols(train, test, FEATURES_FULL)
    cal = fit_ols(train, test, FEATURES_CALENDAR)
    res = full["res"]

    log("\n--- Основная модель (объясняющая):")
    log(str(res.summary()))
    for nm, m in (("Основная модель", full), ("Календарь+температура", cal)):
        mt, mr = m["metrics_test"], m["metrics_train"]
        log(f"{nm:<24} TRAIN: R²={mr['R2']:.4f} | TEST: R²={mt['R2']:.4f}, MAE={mt['MAE']:.3f}, RMSE={mt['RMSE']:.3f}")

    X = full["Xtr"]
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])], index=FEATURES_FULL, name="VIF")
    dw_tr, dw_te = durbin_watson(res.resid), durbin_watson(full["resid_test"])
    jb, jb_p, skew, kurt = jarque_bera(res.resid)
    log("\nМультиколлинеарность (VIF):\n" + vif.round(2).to_string())
    log(f"\nDurbin-Watson: train = {dw_tr:.3f}, test = {dw_te:.3f}")
    log(f"Jarque-Bera: JB = {jb:.1f}, p = {fmt_p(jb_p)}, skew = {skew:.3f}, kurt = {kurt:.3f}")

    sx = train[FEATURES_FULL].std(ddof=1)
    coef = pd.DataFrame({
        "coef": res.params.drop("const"),
        "std_err": res.bse.drop("const"),
        "p_OLS": res.pvalues.drop("const"),
        "p_HAC": full["res_hac"].pvalues.drop("const"),
        "beta_std": res.params.drop("const") * sx / train[TARGET].std(ddof=1),
        "VIF": vif,
    })
    log("\nКоэффициенты:\n" + coef.round(4).to_string())

    # Устойчивость: винсоризация 1%
    hdr("5. ПРОВЕРКА УСТОЙЧИВОСТИ: OLS на винсоризованных данных (1%)")
    bounds = winsor_bounds(train, WINSOR_COLS)
    tr_w, te_w = apply_winsor(train, bounds, WINSOR_COLS), apply_winsor(test, bounds, WINSOR_COLS)
    wfit = fit_ols(tr_w, te_w, FEATURES_FULL, y_test_override=test[TARGET].values)
    cmp_ = pd.DataFrame({"coef_raw": res.params, "coef_winsor": wfit["res"].params})
    cmp_["change_%"] = (cmp_["coef_winsor"] / cmp_["coef_raw"] - 1) * 100
    cmp_["same_sign"] = np.sign(cmp_["coef_raw"]) == np.sign(cmp_["coef_winsor"])
    cmp_["p_winsor"] = wfit["res"].pvalues
    log(cmp_.drop(index="const").round(4).to_string())
    return dict(train=train, test=test, full=full, cal=cal, wfit=wfit, vif=vif, coef=coef, cmp=cmp_,
                diag=dict(dw_train=dw_tr, dw_test=dw_te, jb=jb, jb_p=jb_p, skew=skew, kurt=kurt))

# --------------------------------------------------------------------------- #
# 4. ДАШБОРД
# --------------------------------------------------------------------------- #
def binned_mean(x: pd.Series, y: pd.Series, bins) -> tuple[np.ndarray, np.ndarray]:
    g = pd.DataFrame({"x": x.values, "y": y.values}).groupby(pd.cut(x.values, bins), observed=True)
    out = g.agg(x=("x", "mean"), y=("y", "mean"))
    return out["x"].values, out["y"].values

def build_dashboard(df: pd.DataFrame, reg: dict, out_path: Path) -> dict:
    sns.set_theme(style="whitegrid", context="notebook")
    fig, axes = plt.subplots(3, 2, figsize=(16, 17), constrained_layout=True)
    fig.suptitle("IM-3. Энергопотребление и режимы работы: единая аналитическая панель", fontsize=17, fontweight="bold")
    info: dict = {}

    # 1) Суточный профиль
    ax = axes[0, 0]
    prof = df.groupby(["is_weekend", "hour"])[TARGET].agg(["mean", "sem"]).reset_index()
    for wk, lab, col in ((0, "Будни", "#1f77b4"), (1, "Выходные", "#d62728")):
        p = prof[prof["is_weekend"] == wk]
        ax.plot(p["hour"], p["mean"], marker="o", ms=4, color=col, label=lab)
        ax.fill_between(p["hour"], p["mean"] - 1.96 * p["sem"], p["mean"] + 1.96 * p["sem"], color=col, alpha=0.18)
    ax.set(title="1) Суточный профиль потребления", xlabel="Час суток", ylabel="Среднее Usage_kWh за 15 мин", xticks=range(0, 24, 2))
    ax.legend()
    wd = prof[prof["is_weekend"] == 0].set_index("hour")["mean"]
    we = prof[prof["is_weekend"] == 1].set_index("hour")["mean"]
    info["peak_hour_wd"], info["peak_val_wd"] = int(wd.idxmax()), float(wd.max())
    info["night_mean_wd"] = float(wd.loc[0:5].mean())
    info["we_to_wd"] = float(we.mean() / wd.mean())

    # 2) Распределение
    ax = axes[0, 1]
    grid = np.linspace(0, df[TARGET].max(), 500)
    ax.fill_between(grid, gaussian_kde(df[TARGET])(grid), color="grey", alpha=0.35, label="Все наблюдения")
    for lt in LOAD_ORDER:
        s = df.loc[df["Load_Type"] == lt, TARGET]
        ax.plot(grid, gaussian_kde(s)(grid) * len(s) / len(df), color=LOAD_COLORS[lt], lw=2, label=f"{lt} (доля {len(s) / len(df):.0%})")
    ax.set(title="2) Распределение Usage_kWh (KDE)", xlabel="Usage_kWh за 15 мин", ylabel="Плотность")
    ax.legend()
    info["skew"] = float(df[TARGET].skew())
    info["share_low"] = float((df[TARGET] < 5).mean())

    # 3) Боксплот
    ax = axes[1, 0]
    data = [df.loc[df["Load_Type"] == lt, TARGET].values for lt in LOAD_ORDER]
    bp = ax.boxplot(data, patch_artist=True, flierprops=dict(marker=".", markersize=2, alpha=0.3))
    for patch, lt in zip(bp["boxes"], LOAD_ORDER):
        patch.set_facecolor(LOAD_COLORS[lt]); patch.set_alpha(0.75)
    ax.set_xticks(range(1, 4)); ax.set_xticklabels(LOAD_ORDER)
    ax.set(title="3) Usage_kWh по режимам нагрузки (Load_Type)", ylabel="Usage_kWh за 15 мин")
    info["median_by_load"] = {lt: float(np.median(d)) for lt, d in zip(LOAD_ORDER, data)}
    info["n_fliers"] = {lt: int(len(f.get_ydata())) for lt, f in zip(LOAD_ORDER, bp["fliers"])}

    # 4) Корреляции
    ax = axes[1, 1]
    cols = {TARGET: "Usage_kWh", "Temperature_C": "Температура",
            "Lagging_Current_Reactive_Power_kVarh": "Реакт. (отст.)",
            "Leading_Current_Reactive_Power_kVarh": "Реакт. (опер.)",
            "Lagging_Current_Power_Factor": "PF (отст.)", "Leading_Current_Power_Factor": "PF (опер.)",
            "hour": "Час", "month": "Месяц", "is_weekend": "Выходной"}
    corr = df[list(cols)].corr().rename(index=cols, columns=cols)
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, center=0, square=True, ax=ax, annot_kws={"size": 9})
    ax.set_title("4) Корреляции (Пирсон)")
    info["corr_usage"] = corr["Usage_kWh"].drop("Usage_kWh").sort_values(key=np.abs, ascending=False)

    # 5) Температура
    ax = axes[2, 0]
    ax.scatter(df["Temperature_C"], df[TARGET], s=3, alpha=0.12, color="#1f77b4", rasterized=True)
    bx, by = binned_mean(df["Temperature_C"], df[TARGET], np.arange(-8, 40, 2))
    ax.plot(bx, by, color="#d62728", lw=2.5, marker="o", ms=4, label="Среднее по бинам 2 °C")
    ax.set(title="5) Потребление vs Температура", xlabel="Температура, °C", ylabel="Usage_kWh за 15 мин")
    ax.legend()
    info["r_pearson_T"] = float(df["Temperature_C"].corr(df[TARGET]))
    info["trend_T"] = (float(by[0]), float(by.min()), float(by.max()), float(by[-1]))

    # 6) Остатки
    ax = axes[2, 1]
    fit = reg["full"]
    fv, rs = fit["pred_test"], fit["resid_test"]
    ax.scatter(fv, rs, s=4, alpha=0.25, color="#2ca02c", rasterized=True)
    ax.axhline(0, color="black", lw=1.2)
    ax.set(title="6) Остатки OLS на тесте", xlabel="Предсказанное Usage_kWh", ylabel="Остаток (факт - прогноз)")
    info["resid_bias"] = float(np.mean(rs))
    info["resid_het"] = float(np.corrcoef(np.abs(rs), fv)[0, 1])

    fig.savefig(out_path, dpi=DPI)
    plt.close(fig)
    return info

def panel_comments(info: dict) -> None:
    hdr("4. ПОЯСНЕНИЯ К ГРАФИКАМ ПАНЕЛИ")
    log(f"1) Профиль: пик в будни — {info['peak_hour_wd']:02d}:00 ({info['peak_val_wd']:.1f} кВт·ч). Выходные — {info['we_to_wd']:.0%} от будней.")
    log(f"2) Распределение: асимметрия {info['skew']:.2f}; {info['share_low']:.0%} значений < 5 кВт·ч (простой).")
    log(f"3) Режимы: медианы = " + " / ".join(f"{info['median_by_load'][k]:.1f}" for k in LOAD_ORDER) + " кВт·ч.")
    log(f"4) Корреляции: сильнейшая связь — {info['corr_usage'].index[0]} ({info['corr_usage'].iloc[0]:+.2f}).")
    log(f"5) Температура: Пирсон r = {info['r_pearson_T']:+.2f}. Тренд от {info['trend_T'][0]:.1f} до {info['trend_T'][3]:.1f} кВт·ч.")
    log(f"6) Остатки: смещение {info['resid_bias']:+.2f}; corr(|resid|, pred) = {info['resid_het']:+.2f}.")

# --------------------------------------------------------------------------- #
# 6. СЦЕНАРИЙ ЭКОНОМИИ
# --------------------------------------------------------------------------- #
def savings_scenario(df: pd.DataFrame, n_boot: int = 1000) -> dict:
    hdr("6. СЦЕНАРИЙ: перенос 10% пиковой нагрузки ($0.10/кВт·ч)")
    peak = df["Load_Type"] == "Maximum_Load"
    med = df["Load_Type"] == "Medium_Load"
    e_total = df[TARGET].sum()
    e_peak = df.loc[peak, TARGET].sum()
    e_med = df.loc[med, TARGET].sum()
    e_shift = SHIFT_SHARE * e_peak
    value_shift = e_shift * PRICE_USD_PER_KWH

    daily_peak = df[TARGET].where(peak, 0.0).groupby(df["datetime"].dt.normalize()).sum().values
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(daily_peak), size=(n_boot, len(daily_peak)))
    boot = daily_peak[idx].sum(axis=1) * SHIFT_SHARE * PRICE_USD_PER_KWH
    lo, hi = np.percentile(boot, [2.5, 97.5])

    log(f"Энергия в Maximum_Load: {e_peak:,.0f} кВт·ч ({e_peak / e_total:.1%} всего)")
    log(f"Переносимый объём ({SHIFT_SHARE:.0%} пика): {e_shift:,.0f} кВт·ч -> ${value_shift:,.0f}/год (95% ДИ: ${lo:,.0f} .. ${hi:,.0f})")
    return dict(e_total=e_total, e_peak=e_peak, e_shift=e_shift, value_shift=value_shift,
                ci_low=lo, ci_high=hi, peak_share=e_peak / e_total)

# --------------------------------------------------------------------------- #
# 7. РЕКОМЕНДАЦИИ
# --------------------------------------------------------------------------- #
def recommendations(df: pd.DataFrame, reg: dict, hyp: dict, sc: dict, info: dict) -> list[str]:
    hdr("7. ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ")
    h1 = hyp["H1"]
    cal = reg["cal"]["metrics_test"]
    full = reg["full"]["metrics_test"]
    recs = [
        f"1. Управлять пиками: Maximum_Load даёт {sc['peak_share']:.0%} энергии за {df['Load_Type'].eq('Maximum_Load').mean():.0%} времени; разница с Light = {h1['diff']:.1f} кВт·ч (95% ДИ {h1['ci_low']:.1f}..{h1['ci_high']:.1f}). Эффект переноса: до ${sc['value_shift']:,.0f}/год.",
        f"2. Не опираться на температуру: корреляция r = {info['r_pearson_T']:+.2f}, эффект d = {hyp['H2']['d']:.2f} ({interpret_d(hyp['H2']['d'])}). Базовая регрессия по календарю на тесте имеет R² = {cal['R2']:.2f}. Потребление диктуется графиком.",
        f"3. Использовать реактивную мощность для мониторинга: модель с электрическими параметрами существенно точнее (тест R² = {full['R2']:.2f} против {cal['R2']:.2f} у календаря). Ошибки OLS автокоррелированы (test DW = {reg['diag']['dw_test']:.2f})."
    ]
    for r in recs:
        log(r + "\n")
    return recs

# --------------------------------------------------------------------------- #
# MAIN
# --------------------------------------------------------------------------- #
def _jsonable(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, (pd.DataFrame, pd.Series)):
        return o.to_dict()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)

def main() -> None:
    ap = argparse.ArgumentParser(description="IM-3: энергопотребление промышленного объекта")
    ap.add_argument("--data", default="/content/Hyrasiaone green hydrogen plant data.csv", help="путь к CSV")
    ap.add_argument("--out", default="results", help="каталог результатов")
    args, _ = ap.parse_known_args()  # Интерактивная совместимость для Colab
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df, audit = load_and_audit(Path(args.data))
    df[[TARGET, "Temperature_C", "Lagging_Current_Reactive_Power_kVarh",
        "Leading_Current_Reactive_Power_kVarh", "Lagging_Current_Power_Factor",
        "Leading_Current_Power_Factor"]].describe().T.to_csv(out / "descriptive_stats.csv", encoding="utf-8-sig")

    hyp = run_hypotheses(df)
    reg = run_regression(df)
    info = build_dashboard(df, reg, out / "fig_panel_6.png")
    panel_comments(info)
    sc = savings_scenario(df)
    recs = recommendations(df, reg, hyp, sc, info)

    reg["coef"].to_csv(out / "ols_coefficients.csv", encoding="utf-8-sig")
    reg["cmp"].to_csv(out / "robustness_coefficients.csv", encoding="utf-8-sig")

    summary = dict(
        audit=audit, hypotheses=hyp, diagnostics=reg["diag"],
        metrics_test_full=reg["full"]["metrics_test"], metrics_test_calendar=reg["cal"]["metrics_test"],
        metrics_test_winsor=reg["wfit"]["metrics_test"], metrics_train_full=reg["full"]["metrics_train"],
        scenario=sc, recommendations=recs,
    )
    (out / "results_summary.json").write_text(json.dumps(summary, default=_jsonable, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "analysis_report.txt").write_text("\n".join(_LOG), encoding="utf-8")
    log(f"\nГотово. Файлы сохранены в каталог: {out.resolve()}")

if __name__ == "__main__":
    main()
