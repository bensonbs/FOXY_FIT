chcp 65001
@echo off
set VENV_NAME=foxyfit_venv
if not defined VENV_DIR (set "VENV_DIR=%~dp0%foxyfit_venv")
set PYTHON="%VENV_DIR%\Scripts\Python.exe"
echo venv %PYTHON%
call %VENV_NAME%\Scripts\activate
streamlit run main.py
pause