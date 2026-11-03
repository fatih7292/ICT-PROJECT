"""
LOG ANALYTICS — веб-интерфейс на Streamlit с авторизацией по Face ID.
 
Запуск:
    pip install streamlit pandas plotly deepface tf-keras opencv-python
    streamlit run app.py
"""
 
import base64
import os
from pathlib import Path
 
import pandas as pd
import plotly.express as px
import streamlit as st
from deepface import DeepFace
 
import costs
 
# ------------------------------------------------------------------
# 1. Базовая настройка страницы
# ------------------------------------------------------------------
 
st.set_page_config(
    page_title="LOG ANALYTICS",
    page_icon="🚚",
    layout="wide",
)
 
BASE_DIR = Path(__file__).parent
AVATAR_PATH = BASE_DIR / "photo_5291985963577973198_w.jpg"
MY_FACE_PATH = BASE_DIR / "my_face.jpg"  # Файл с вашим эталонным фото
 
 
# ------------------------------------------------------------------
# 2. АВТОРИЗАЦИЯ ПО FACE ID (эталон: my_face.jpg)
# ------------------------------------------------------------------
 
import cv2
import numpy as np
 
 
# Порог совпадения (косинусное расстояние, модель Facenet512).
# Чем БОЛЬШЕ число — тем мягче проверка. Стандарт DeepFace = 0.30.
#   0.30 — строго | 0.40 — мягко | 0.50 — очень мягко | 0.60+ — пустит и похожих людей
FACE_THRESHOLD = 0.49
 
# Строгая проверка «в кадре действительно лицо»:
FACE_DETECTORS = ("retinaface", "ssd")   # надёжнее, чем простой opencv
MIN_FACE_CONFIDENCE = 0.90               # уверенность детектора (0..1)
MIN_FACE_WIDTH_RATIO = 0.15              # ширина лица не меньше 15% ширины кадра
 
 
def load_image(path: Path) -> tuple["np.ndarray | None", str]:
    """Читает фото в формате BGR. Возвращает (картинка, причина_ошибки)."""
    try:
        # np.fromfile + imdecode работает и с кириллицей в пути (в отличие от cv2.imread)
        data = np.fromfile(str(path), dtype=np.uint8)
    except OSError as e:
        return None, f"не удалось прочитать файл ({e})"
 
    if data.size == 0:
        return None, "файл пустой (0 байт) — скопируйте фото заново"
 
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is not None:
        return img, ""
 
    # Запасной вариант: Pillow (понимает WebP, и HEIC при наличии pillow-heif)
    try:
        from PIL import Image
 
        try:
            import pillow_heif 
            pillow_heif.register_heif_opener()
        except ImportError:
            pass
 
        pil_img = Image.open(path).convert("RGB")
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR), ""
    except Exception as e:
        return None, (
            f"формат не распознан ({e}). Если фото с iPhone — это, скорее всего, HEIC: "
            "выполните `pip install pillow-heif` или пересохраните снимок как настоящий JPG"
        )
 
 
def enhance(img: "np.ndarray") -> "np.ndarray":
    """Улучшает снимок со слабой камеры: увеличивает размер и выравнивает освещение."""
    h, w = img.shape[:2]
    if w < 800:
        scale = 800 / w
        img = cv2.resize(img, (800, int(h * scale)), interpolation=cv2.INTER_CUBIC)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
 
 
def reference_paths() -> list[Path]:
    """my_face.jpg + любые дополнительные эталоны: my_face_2.jpg, my_face_cam.jpg и т.д."""
    extra = sorted(BASE_DIR.glob("my_face_*.jpg"))
    return [p for p in [MY_FACE_PATH, *extra] if p.exists()]
 
 
def find_valid_face(img: "np.ndarray") -> tuple["str | None", str]:
    """Ищет в кадре полноценное лицо. Возвращает (детектор, причина_отказа).
 
    Лицо принимается, только если: высокая уверенность детектора, видны оба глаза,
    лицо достаточно крупное и находится ближе к центру кадра.
    """
    h, w = img.shape[:2]
    reason = "Лицо в кадре не найдено. Встаньте напротив камеры, откройте лицо."
 
    for detector in FACE_DETECTORS:
        try:
            faces = DeepFace.extract_faces(
                img_path=img,
                detector_backend=detector,
                enforce_detection=True,
                align=True,
            )
        except Exception:
            continue
 
        # берём самое крупное лицо
        face = max(faces, key=lambda f: f["facial_area"]["w"] * f["facial_area"]["h"])
        fa = face["facial_area"]
 
        if face.get("confidence", 1.0) < MIN_FACE_CONFIDENCE:
            reason = "Лицо видно плохо или закрыто. Откройте лицо и добавьте света."
            continue
        if not (fa.get("left_eye") and fa.get("right_eye")):
            reason = "Не видны оба глаза. Снимите маску/руки, смотрите в камеру."
            continue
        if fa["w"] / w < MIN_FACE_WIDTH_RATIO:
            reason = "Лицо слишком маленькое. Придвиньтесь ближе к камере."
            continue
        cx, cy = fa["x"] + fa["w"] / 2, fa["y"] + fa["h"] / 2
        if not (0.25 * w <= cx <= 0.75 * w and 0.2 * h <= cy <= 0.8 * h):
            reason = "Лицо не по центру. Встаньте напротив камеры."
            continue
 
        return detector, ""
 
    return None, reason
 
 
def verify_face(img_bytes: bytes) -> tuple[bool, str]:
    """Проверяет, что в кадре настоящее лицо, затем сравнивает с эталонами."""
    live = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    if live is None:
        return False, "Не удалось прочитать снимок с камеры."
 
    refs = []
    for path in reference_paths():
        img, err = load_image(path)
        if img is None:
            return False, f"Не удалось открыть {path.name}: {err}"
        refs.append(img)
 
    # 1. Строгая проверка наличия лица (исходный кадр, затем улучшенный)
    detector, reason, face_img = None, "", None
    for candidate in (live, enhance(live)):
        detector, reason = find_valid_face(candidate)
        if detector:
            face_img = candidate
            break
    if detector is None:
        return False, reason
 
    # 2. Сравнение с эталонами
    best = None
    for ref in refs:
        try:
            result = DeepFace.verify(
                img1_path=face_img,
                img2_path=ref,
                model_name="Facenet512",
                detector_backend=detector,
                distance_metric="cosine",
                enforce_detection=True,
            )
        except ValueError:
            continue
        d = result.get("distance", 1.0)
        best = d if best is None else min(best, d)
 
    if best is None:
        return False, "Не удалось найти лицо на эталонном фото."
    if best <= FACE_THRESHOLD:
        return True, f"Доступ разрешён (расстояние {best:.2f})."
    return False, (
        f"Доступ запрещён: лицо не совпадает с эталоном "
        f"(расстояние {best:.2f}, нужно ≤ {FACE_THRESHOLD})."
    )
 
 
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
 
if not st.session_state["authenticated"]:
    st.title("🔒 Вход в систему LOG ANALYTICS")
    st.write("Доступ ограничен. Пожалуйста, пройдите проверку лица.")
 
    if not MY_FACE_PATH.exists():
        st.error(f"Файл {MY_FACE_PATH.name} не найден! Положите фото в папку с проектом.")
        st.stop()
 
    img_buffer = st.camera_input("Скан лица для авторизации")
 
    if img_buffer is not None:
        with st.spinner("Сравнение биометрии..."):
            ok, message = verify_face(img_buffer.getvalue())
        if ok:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error(f"❌ {message}")
 
    # Всё, что ниже, не выполнится без успешного входа
    st.stop()


# ------------------------------------------------------------------
# 3. Вспомогательные функции и CSS
# ------------------------------------------------------------------

def img_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


AVATAR_B64 = img_to_base64(AVATAR_PATH)

st.markdown(
    """
    <style>
    :root {
        --primary: #8a9e9e;
        --primary-dark: #6b7d7d;
        --primary-light: #a8b8b8;
        --bg: #f0f3f3;
        --card-bg: #ffffff;
        --text: #1a2e2e;
        --text-light: #4a5e5e;
        --border: #c8d0d0;
        --success: #4caf50;
        --warning: #ff9800;
        --error: #f44336;
        --shadow: 0 4px 20px rgba(0,0,0,0.08);
        --shadow-hover: 0 8px 30px rgba(0,0,0,0.12);
    }

    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
    body, .stApp { background: var(--bg); }

    .log-header {
        position: relative;
        background: var(--primary);
        border-radius: 18px;
        padding: 24px 40px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .log-logo-block { display: flex; flex-direction: column; }
    .log-logo {
        font-size: 3rem;
        font-weight: 900;
        color: #000;
        letter-spacing: -2px;
        text-transform: uppercase;
        line-height: 1;
        margin: 0;
    }
    .log-logo-sub-strong {
        font-size: 1rem;
        font-weight: 700;
        color: #10251f;
        letter-spacing: 2px;
        margin-top: 2px;
    }
    .log-logo-subtitle {
        font-size: 0.85rem;
        color: rgba(0,0,0,0.6);
        font-weight: 500;
        letter-spacing: 1px;
        margin-top: 6px;
    }
    .log-admin-profile {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 16px;
        border-radius: 12px;
    }
    .log-avatar-wrapper { position: relative; width: 56px; height: 56px; }
    .log-avatar {
        width: 100%; height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #fff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .log-status-indicator {
        position: absolute; bottom: 2px; right: 2px;
        width: 14px; height: 14px;
        background: var(--success);
        border-radius: 50%;
        border: 2px solid #fff;
    }
    .log-admin-info { display: flex; flex-direction: column; }
    .log-admin-name { font-size: 1.05rem; font-weight: 700; color: #000; }
    .log-admin-role { font-size: 0.8rem; color: rgba(0,0,0,0.6); }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: var(--shadow);
        border-top: 4px solid var(--primary);
        transition: all 0.25s ease;
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-hover); }
    .kpi-card.warning { border-top-color: var(--warning); }
    .kpi-card.error { border-top-color: var(--error); }
    .kpi-label {
        font-size: 0.8rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: var(--text);
        line-height: 1.1;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 6px 0 16px 0;
        color: var(--text);
    }

    .terminal-box {
        background: #10251f;
        color: #7CFC9A;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 0.92rem;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: var(--shadow);
        white-space: pre-wrap;
        line-height: 1.5;
        margin-bottom: 30px;
    }
    .terminal-box .prompt { color: #8a9e9e; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------

avatar_html = (
    f'<img src="data:image/jpeg;base64,{AVATAR_B64}" class="log-avatar">'
    if AVATAR_B64
    else '<div class="log-avatar" style="background:#ccc;"></div>'
)

st.markdown(
    f"""
    <div class="log-header">
        <div class="log-logo-block">
            <h1 class="log-logo">LOG</h1>
            <div class="log-logo-sub-strong">ANALYTICS</div>
            <span class="log-logo-subtitle">Анализ логистических затрат и транспортных маршрутов</span>
        </div>
        <div class="log-admin-profile">
            <div class="log-avatar-wrapper">
                {avatar_html}
                <span class="log-status-indicator"></span>
            </div>
            <div class="log-admin-info">
                <span class="log-admin-name">Оператор</span>
                <span class="log-admin-role">Аналитик</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Загрузка данных
# ------------------------------------------------------------------

@st.cache_data
def get_data() -> pd.DataFrame:
    df = costs.load_data()
    df = costs.add_kpi_columns(df)
    return df


try:
    raw_df = get_data()
except FileNotFoundError as e:
    st.error(f"Не найден файл с данными: {e}")
    st.stop()


# ------------------------------------------------------------------
# Сайдбар — фильтры
# ------------------------------------------------------------------

st.sidebar.header("Фильтры")

min_date, max_date = raw_df["Дата"].min(), raw_df["Дата"].max()
date_range = st.sidebar.date_input(
    "Период",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

carriers = sorted(raw_df["Перевозчик"].unique())
selected_carriers = st.sidebar.multiselect("Перевозчик", carriers, default=carriers)

regions = sorted(set(raw_df["Регион_отправления"]) | set(raw_df["Регион_назначения"]))
selected_regions = st.sidebar.multiselect("Регион (отправления или назначения)", regions, default=[])

threshold = st.sidebar.slider("Порог аномалии тарифа, %", 5, 50, 15)

df = raw_df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    df = df[(df["Дата"].dt.date >= start) & (df["Дата"].dt.date <= end)]

if selected_carriers:
    df = df[df["Перевозчик"].isin(selected_carriers)]

if selected_regions:
    df = df[
        df["Регион_отправления"].isin(selected_regions)
        | df["Регион_назначения"].isin(selected_regions)
    ]

if df.empty:
    st.warning("Нет рейсов по выбранным фильтрам.")
    st.stop()


# ------------------------------------------------------------------
# KPI-карточки
# ------------------------------------------------------------------

total_cost = df["Стоимость_тенге"].sum()
total_ton_km = df["Грузооборот_ткм"].sum()
avg_rate = df["Стоимость_за_ткм"].mean()
n_trips = len(df)
n_overpriced = (df["Отклонение_от_среднего_%"] > threshold).sum()

st.markdown('<div class="section-title">Ключевые показатели</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Суммарные затраты</div>
            <div class="kpi-value">{total_cost:,.0f} ₸</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Грузооборот</div>
            <div class="kpi-value">{total_ton_km:,.0f} т·км</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средний тариф</div>
            <div class="kpi-value">{avg_rate:,.2f} ₸/т·км</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Всего рейсов</div>
            <div class="kpi-value">{n_trips:,}</div>
        </div>
        <div class="kpi-card warning">
            <div class="kpi-label">Рейсов с завышенным тарифом (&gt;{threshold}%)</div>
            <div class="kpi-value">{n_overpriced}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# "Терминальный" вывод — вывод из costs.py
# ------------------------------------------------------------------

st.markdown('<div class="section-title">Вывод программы (как в консоли)</div>', unsafe_allow_html=True)

report_text = costs.summary_report(df)
overpriced = costs.find_overpriced_trips(df, threshold_pct=threshold)

terminal_text = (
    "<span class='prompt'>$ python costs.py</span>\n\n"
    + report_text
    + f"\n=== Топ-10 рейсов с превышением тарифа (>{threshold}%) ===\n"
    + overpriced.head(10).to_string(index=False)
)

st.markdown(f'<div class="terminal-box">{terminal_text}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------
# Таблицы и графики
# ------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Затраты по перевозчикам</div>', unsafe_allow_html=True)
    by_carrier = costs.costs_by_carrier(df)
    st.dataframe(by_carrier, use_container_width=True)

    fig_carrier = px.bar(
        by_carrier.reset_index(),
        x="Перевозчик",
        y="Общая_стоимость_тенге",
        color="Перевозчик",
        title="Затраты по перевозчикам, тенге",
    )
    fig_carrier.update_layout(showlegend=False, plot_bgcolor="white")
    st.plotly_chart(fig_carrier, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">Затраты по виду транспорта</div>', unsafe_allow_html=True)
    by_transport = costs.costs_by_transport_type(df)
    st.dataframe(by_transport, use_container_width=True)

    fig_transport = px.pie(
        by_transport.reset_index(),
        names="Вид_транспорта",
        values="Общая_стоимость_тенге",
        title="Доля затрат по виду транспорта",
    )
    st.plotly_chart(fig_transport, use_container_width=True)

st.markdown('<div class="section-title">Динамика затрат по месяцам</div>', unsafe_allow_html=True)
by_month = costs.costs_by_month(df).reset_index()
fig_month = px.line(
    by_month, x="Месяц", y="Общая_стоимость_тенге", markers=True,
    title="Суммарные затраты по месяцам, тенге",
)
fig_month.update_layout(plot_bgcolor="white")
st.plotly_chart(fig_month, use_container_width=True)

st.markdown('<div class="section-title">Рейсы с завышенным тарифом</div>', unsafe_allow_html=True)
st.dataframe(overpriced, use_container_width=True)