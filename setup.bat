chcp 65001
@echo off

set VENV_NAME=foxyfit_venv
set PYTHON_EXE=python

REM 下載並安裝依賴包
if exist %VENV_NAME% (
    echo %VENV_NAME% 已存在。
) else (
    REM 創建虛擬環境
	echo 正在創建虛擬環境：%VENV_NAME%
	%PYTHON_EXE% -m venv %VENV_NAME%

	echo 虛擬環境創建成功。

	call %VENV_NAME%\Scripts\activate
    echo 安裝相依套件
    pip install --trusted-host 10.3.141.1 --index-url http://10.3.141.1:3000/api/packages/bensonbssung/pypi/simple -r requirements-1.txt
    pip install --trusted-host 10.3.141.1 --index-url http://10.3.141.1:3000/api/packages/bensonbssung/pypi/simple -r requirements-2.txt
)

echo 安裝完成.
pause