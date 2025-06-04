@echo off
chcp 65001 >nul
echo ==========================================
echo  Python 설치 가이드
echo  (Algorithm Visualizer 사전 준비)
echo ==========================================
echo.

echo 🔍 Python 설치 상태 확인 중...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python이 설치되지 않았습니다!
    echo.
    echo 📋 Python 설치 방법 (선택하세요):
    echo.
    
    REM winget 확인
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo 🚀 방법 1: winget 자동 설치 (추천 - Microsoft 공식)
        echo    winget install Python.Python.3.11
        echo.
    )
    
    REM Chocolatey 확인
    choco --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo 🍫 방법 2: Chocolatey 자동 설치
        echo    choco install python311
        echo.
    )
    
    echo 🏪 방법 3: Windows Store 설치
    echo    1. 윈도우키 + R 누르기
    echo    2. 다음 명령어 복사해서 붙여넣기:
    echo       ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo    3. Enter 키 누르고 Python 설치
    echo.
    echo 📥 방법 4: 수동 설치 (공식 사이트)
    echo    1. https://www.python.org/downloads/ 방문
    echo    2. "Download Python 3.11" 버튼 클릭
    echo    3. 설치 시 "Add Python to PATH" 체크박스 반드시 선택!
    echo.
    
    echo 🔧 패키지 매니저가 없는 경우:
    echo.
    echo 📦 winget 설치 (Windows 10 1709+ / Windows 11):
    echo    1. Microsoft Store에서 "App Installer" 설치
    echo    2. 또는 https://aka.ms/getwinget 방문
    echo.
    echo 🍫 Chocolatey 설치:
    echo    1. PowerShell을 관리자 권한으로 실행
    echo    2. 다음 명령어 실행:
    echo       Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    echo.
    echo 🪣 Scoop 설치 (가장 간단):
    echo    1. PowerShell에서 실행:
    echo       iwr -useb get.scoop.sh | iex
    echo    2. 그 후: scoop install python
    echo.
    echo ⚠️  중요사항:
    echo    - 어떤 방법으로 설치하든 PATH 설정이 중요합니다
    echo    - 설치 후 새 명령 프롬프트를 열어 테스트하세요
    echo    - 기업 환경에서는 IT 관리자에게 문의하세요
    echo.
    echo Python 설치 완료 후 setup_windows.bat을 실행하세요.
    echo.
) else (
    echo ✅ Python이 이미 설치되어 있습니다!
    python --version
    echo.
    echo 🎉 setup_windows.bat 스크립트를 실행할 수 있습니다!
    echo.
)

pause 