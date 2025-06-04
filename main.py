#!/usr/bin/env python3
"""
Algorithm Visualizer - 탐색 알고리즘 시각화
DFS, BFS 알고리즘의 동작을 시각적으로 학습할 수 있는 프로그램

실행 방법:
    python main.py
    또는
    .venv/Scripts/python.exe main.py  (Windows)
    .venv/bin/python main.py         (Linux/macOS)

작성자: Algorithm Visualizer Team
버전: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 현재 스크립트의 디렉토리를 모듈 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def check_dependencies():
    """필요한 패키지들이 설치되어 있는지 확인"""
    required_packages = [
        ('matplotlib', 'matplotlib'),
        ('networkx', 'networkx'), 
        ('numpy', 'numpy'),
        ('PIL', 'Pillow')
    ]
    
    missing_packages = []
    
    for package_name, install_name in required_packages:
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(install_name)
    
    if missing_packages:
        error_msg = f"""
필요한 패키지가 설치되지 않았습니다:
{', '.join(missing_packages)}

다음 명령어로 설치해주세요:
pip install {' '.join(missing_packages)}

또는 가상환경을 사용하는 경우:
uv sync
"""
        print(error_msg)
        
        # GUI 환경에서는 메시지박스로 표시
        try:
            root = tk.Tk()
            root.withdraw()  # 메인 윈도우 숨기기
            messagebox.showerror("패키지 누락", error_msg)
            root.destroy()
        except:
            pass
        
        return False
    
    return True

def setup_matplotlib_korean():
    """matplotlib 한글 폰트 설정"""
    try:
        from utils.font_utils import FontUtils
        
        print("🔤 한글 폰트를 설정하는 중...")
        success = FontUtils.setup_korean_font()
        
        if success:
            print("✅ 한글 폰트 설정이 완료되었습니다.")
        else:
            print("⚠️ 한글 폰트 설정에 문제가 있을 수 있습니다.")
            print("   일부 텍스트가 깨져 보일 수 있습니다.")
        
        return True
        
    except Exception as e:
        print(f"⚠️ 폰트 설정 중 오류 발생: {e}")
        print("   프로그램은 계속 실행되지만 한글이 깨져 보일 수 있습니다.")
        return False

def main():
    """메인 함수"""
    print("=" * 50)
    print("Algorithm Visualizer - 탐색 알고리즘 시각화")
    print("=" * 50)
    print("DFS, BFS 알고리즘의 동작을 시각적으로 학습하세요!")
    print()
    
    # 의존성 확인
    print("필요한 패키지들을 확인하는 중...")
    if not check_dependencies():
        print("❌ 패키지 설치 후 다시 실행해주세요.")
        return 1
    
    print("✅ 모든 패키지가 설치되어 있습니다.")
    print()
    
    # 한글 폰트 설정
    setup_matplotlib_korean()
    print()
    
    # GUI 애플리케이션 시작
    try:
        from gui.main_window import MainWindow
        
        print("🚀 Algorithm Visualizer를 시작합니다...")
        print()
        print("사용법:")
        print("1. 상단에서 그래프 유형을 선택하세요 (샘플 그래프, 이진 트리, 미로)")
        print("2. 알고리즘을 선택하세요 (DFS 또는 BFS)")
        print("3. 시작 노드와 목표 노드를 선택하세요")
        print("4. '시작' 버튼을 클릭하여 시각화를 시작하세요")
        print("5. 애니메이션 속도를 조절하거나 단계별로 실행할 수 있습니다")
        print()
        
        # 메인 윈도우 생성 및 실행
        app = MainWindow()
        app.run()
        
        print("👋 Algorithm Visualizer를 종료합니다.")
        return 0
        
    except ImportError as e:
        error_msg = f"모듈 로드 실패: {e}\n프로젝트 구조를 확인해주세요."
        print(f"❌ {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("모듈 오류", error_msg)
            root.destroy()
        except:
            pass
        
        return 1
        
    except Exception as e:
        error_msg = f"애플리케이션 실행 중 오류가 발생했습니다: {e}"
        print(f"❌ {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("실행 오류", error_msg)
            root.destroy()
        except:
            pass
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
