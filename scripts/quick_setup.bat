@echo off
chcp 65001 >nul
echo 🚀 빠른 설치 중... (자세한 로그는 setup_windows.bat 사용)
pip install uv >nul 2>&1
uv python install 3.11 >nul 2>&1
uv sync >nul 2>&1
echo ✅ 설치 완료! 
echo 실행: .venv\Scripts\python.exe main.py
pause 