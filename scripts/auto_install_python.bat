@echo off
chcp 65001 >nul
echo ==========================================
echo  Python 자동 설치 스크립트
echo  (Algorithm Visualizer)
echo ==========================================
echo.

echo 🔍 Python 설치 상태 확인 중...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python이 이미 설치되어 있습니다!
    python --version
    echo.
    echo 🎉 setup_windows.bat 스크립트를 실행할 수 있습니다!
    pause
    exit /b 0
)

echo ❌ Python이 설치되지 않았습니다. 자동 설치를 시작합니다...
echo.

REM winget으로 설치 시도
echo 🚀 winget으로 Python 설치 시도 중...
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    if %errorlevel% equ 0 (
        echo ✅ winget으로 Python 설치 완료!
        echo.
        echo 🔄 PATH 업데이트를 위해 새 명령 프롬프트를 열어주세요.
        echo 그 후 setup_windows.bat을 실행하세요.
        pause
        exit /b 0
    )
    echo ⚠️ winget 설치 실패. 다른 방법을 시도합니다...
    echo.
)

REM Chocolatey로 설치 시도
echo 🍫 Chocolatey로 Python 설치 시도 중...
choco --version >nul 2>&1
if %errorlevel% equ 0 (
    choco install python311 -y
    if %errorlevel% equ 0 (
        echo ✅ Chocolatey로 Python 설치 완료!
        echo.
        echo 🔄 PATH 업데이트를 위해 새 명령 프롬프트를 열어주세요.
        echo 그 후 setup_windows.bat을 실행하세요.
        pause
        exit /b 0
    )
    echo ⚠️ Chocolatey 설치 실패. 다른 방법을 시도합니다...
    echo.
)

REM 자동 설치 실패
echo.
echo ❌ 자동 설치에 실패했습니다.
echo.
echo 📋 수동 설치 방법:
echo.
echo 🏪 Windows Store (가장 쉬움):
echo    1. 윈도우키 + R 누르기
echo    2. 다음 명령어 복사/붙여넣기: ms-windows-store://pdp/?ProductId=9NRWMJP3717K
echo    3. Enter 키 누르고 Python 설치
echo.
echo 📥 공식 사이트:
echo    1. https://www.python.org/downloads/ 방문
echo    2. "Download Python 3.11" 클릭
echo    3. 설치 시 "Add Python to PATH" 반드시 체크!
echo.
echo 🔧 패키지 매니저 설치 후 다시 시도:
echo    - winget: Microsoft Store에서 "App Installer" 설치
echo    - Chocolatey: install_python_first.bat 참조
echo.
pause 