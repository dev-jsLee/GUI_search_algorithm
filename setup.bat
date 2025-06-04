@echo off
chcp 65001 >nul
echo ==========================================
echo  Algorithm Visualizer 설치
echo  한 번의 클릭으로 모든 설정 완료!
echo ==========================================
echo.

REM Python 설치 상태 및 버전 확인
echo 🔍 Python 설치 상태 확인 중...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo.
    echo 🤖 Python을 자동으로 설치하시겠습니까? (Y/N)
    set /p choice="선택: "
    
    if /i "%choice%"=="Y" (
        echo.
        echo 🚀 Python 자동 설치를 시작합니다...
        call scripts\auto_install_python.bat
        
        REM 자동 설치 후 다시 확인
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo.
            echo ⚠️ 자동 설치가 완료되지 않았습니다.
            echo 수동 설치 안내를 확인해주세요.
            call scripts\install_python_first.bat
            exit /b 1
        )
    ) else (
        echo.
        echo 📋 Python 설치 안내를 표시합니다...
        call scripts\install_python_first.bat
        exit /b 1
    )
)

REM Python 버전 확인
echo ✅ Python이 설치되어 있습니다.
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 현재 버전: %PYTHON_VERSION%

REM Python 3.11 버전 확인
echo %PYTHON_VERSION% | findstr /C:"3.11" >nul
if %errorlevel% equ 0 (
    echo ✅ Python 3.11 버전이 확인되었습니다!
    goto :install_project
) else (
    echo.
    echo ⚠️ Python %PYTHON_VERSION%이 설치되어 있지만, 3.11 버전이 아닙니다.
    echo.
    echo 🔄 Python 3.11을 추가로 설치하고 가상환경을 구성하시겠습니까? (Y/N)
    set /p choice="선택: "
    
    if /i "%choice%"=="Y" (
        echo.
        echo 🚀 Python 3.11 설치 및 프로젝트 설정을 진행합니다...
        call scripts\setup_windows.bat
        exit /b %errorlevel%
    ) else (
        echo.
        echo ℹ️ 기존 Python 버전으로 설치를 진행합니다.
        echo   (일부 기능이 정상 동작하지 않을 수 있습니다)
        goto :install_project
    )
)

:install_project
echo.
echo 🎯 가상환경 생성 및 의존성 설치를 시작합니다...
echo.

REM uv 설치 확인 및 설치
echo [1/4] uv 설치 확인 중...
uv --version >nul 2>&1
if %errorlevel% nequ 0 (
    echo uv 설치 중...
    pip install uv >nul 2>&1
    if %errorlevel% nequ 0 (
        echo ❌ uv 설치 실패! 인터넷 연결을 확인해주세요.
        pause
        exit /b 1
    )
    echo ✅ uv 설치 완료
) else (
    echo ✅ uv가 이미 설치되어 있습니다
)

echo.
echo [2/4] Python 3.11 확인 중...
uv python install 3.11 >nul 2>&1
if %errorlevel% nequ 0 (
    echo ⚠️ Python 3.11 설치 중 문제가 발생했습니다. 기존 Python으로 진행합니다.
) else (
    echo ✅ Python 3.11 준비 완료
)

echo.
echo [3/4] 가상환경 생성 및 패키지 설치 중...
uv sync >nul 2>&1
if %errorlevel% nequ 0 (
    echo ❌ 가상환경 생성 실패!
    echo 상세한 로그를 확인하려면 scripts\setup_windows.bat을 실행해주세요.
    pause
    exit /b 1
)

echo.
echo [4/4] 설치 확인 중...
.venv\Scripts\python.exe --version >nul 2>&1
if %errorlevel% nequ 0 (
    echo ❌ 가상환경 확인 실패!
    pause
    exit /b 1
)

.venv\Scripts\python.exe -c "import matplotlib, numpy, networkx; print('패키지 확인 완료!')" >nul 2>&1
if %errorlevel% nequ 0 (
    echo ⚠️ 일부 패키지가 누락되었을 수 있습니다.
) else (
    echo ✅ 모든 패키지 설치 확인 완료!
)

echo.
echo ==========================================
echo 🎉 설치가 완료되었습니다!
echo ==========================================
echo.
echo 📋 프로그램 실행 방법:
echo    .venv\Scripts\python.exe main.py
echo.
echo 📂 추가 스크립트:
echo    scripts\ 폴더에서 개별 설치 스크립트 확인 가능
echo.
pause 