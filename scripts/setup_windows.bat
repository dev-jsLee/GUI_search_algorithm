@echo off
chcp 65001 >nul
echo ==========================================
echo  Algorithm Visualizer 설치 스크립트
echo  Windows 버전
echo ==========================================
echo.

echo [0/6] Python 설치 확인 중...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python이 설치되지 않았습니다!
    echo.
    echo 🤖 자동 설치를 시도해볼까요? (Y/N)
    set /p choice="선택: "
    
    if /i "%choice%"=="Y" (
        echo.
        echo 🚀 Python 자동 설치 시도 중...
        
        REM winget으로 설치 시도
        winget --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo winget으로 Python 설치 중...
            winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements >nul 2>&1
            if %errorlevel% equ 0 (
                echo ✅ winget으로 Python 설치 성공!
                echo 🔄 PATH 업데이트를 위해 잠시 기다려주세요...
                timeout /t 3 >nul
                goto :python_check_retry
            )
        )
        
        REM Chocolatey로 설치 시도
        choco --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo Chocolatey로 Python 설치 중...
            choco install python311 -y >nul 2>&1
            if %errorlevel% equ 0 (
                echo ✅ Chocolatey로 Python 설치 성공!
                echo 🔄 PATH 업데이트를 위해 잠시 기다려주세요...
                timeout /t 3 >nul
                goto :python_check_retry
            )
        )
        
        echo ⚠️ 자동 설치 실패. 수동 설치가 필요합니다.
        echo.
    )
    
    echo 📋 Python 수동 설치 방법:
    echo.
    echo 🚀 방법 1: winget (추천)
    echo    winget install Python.Python.3.11
    echo.
    echo 🍫 방법 2: Chocolatey
    echo    choco install python311
    echo.
    echo 🏪 방법 3: Windows Store
    echo    윈도우키 + R → ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo.
    echo 📥 방법 4: 공식 사이트
    echo    https://www.python.org/downloads/
    echo    설치 시 "Add Python to PATH" 체크박스 반드시 선택!
    echo.
    echo Python 설치 완료 후 이 스크립트를 다시 실행해주세요.
    echo.
    pause
    exit /b 1

:python_check_retry
    REM PATH 새로고침 후 다시 확인
    call refreshenv >nul 2>&1
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Python 설치는 완료되었지만 PATH 설정이 아직 적용되지 않았습니다.
        echo 새 명령 프롬프트를 열고 다시 실행해주세요.
        pause
        exit /b 1
    )
) else (
    echo ✅ Python이 설치되어 있습니다.
    python --version
)

echo.
echo [1/6] uv 설치 확인 중...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv가 설치되지 않았습니다. 설치 중...
    
    REM pip을 통한 설치 시도
    pip install uv >nul 2>&1
    if %errorlevel% neq 0 (
        echo pip 설치 실패. 대안 방법으로 설치 중...
        
        REM PowerShell을 통한 직접 설치 시도
        powershell -Command "& {Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression}" >nul 2>&1
        if %errorlevel% neq 0 (
            echo.
            echo ❌ uv 설치 실패!
            echo.
            echo 📋 수동 설치 방법:
            echo    1. pip install uv
            echo    2. 또는 https://docs.astral.sh/uv/getting-started/installation/ 참조
            echo.
            pause
            exit /b 1
        )
    )
    echo ✅ uv 설치 완료
) else (
    echo ✅ uv가 이미 설치되어 있습니다.
)

echo.
echo [2/6] Python 3.11 설치 중...
uv python install 3.11
if %errorlevel% neq 0 (
    echo ❌ Python 3.11 설치 실패!
    pause
    exit /b 1
)
echo ✅ Python 3.11 설치 완료

echo.
echo [3/6] 가상환경 생성 및 의존성 설치 중...
uv sync
if %errorlevel% neq 0 (
    echo ❌ 가상환경 생성 또는 의존성 설치 실패!
    pause
    exit /b 1
)
echo ✅ 가상환경 및 의존성 설치 완료

echo.
echo [4/6] 설치 확인 중...
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -c "import matplotlib, numpy, networkx; print('✅ 모든 패키지 정상 설치됨')"
if %errorlevel% neq 0 (
    echo ❌ 패키지 설치 확인 실패!
    pause
    exit /b 1
)

echo.
echo [5/6] 설치 완료!
echo ==========================================
echo.
echo 🎉 설치가 성공적으로 완료되었습니다!
echo.
echo 📋 프로그램 실행 방법:
echo    방법 1: .venv\Scripts\python.exe main.py
echo    방법 2: .venv\Scripts\activate 후 python main.py
echo.
echo ⚠️  PowerShell 실행 정책 오류가 발생하는 경우:
echo    PowerShell을 관리자 권한으로 실행 후
echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo.
echo ==========================================
echo.
pause 