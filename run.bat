@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo Запуск системы LOG ANALYTICS...
py -m streamlit run app.py
pause