# 알고리즘 시각화 프로그램 (Algorithm Visualizer)

## 📋 프로젝트 개요
Python 수업에서 사용할 수 있는 교육용 알고리즘 시각화 프로그램입니다. 
특히 **탐색 알고리즘(DFS, BFS)**을 중심으로 알고리즘의 동작 과정을 시각적으로 이해할 수 있도록 설계되었습니다.

## 🎯 학습 목표
- 깊이 우선 탐색(DFS)과 너비 우선 탐색(BFS)의 차이점 이해
- 각 알고리즘의 탐색 순서와 패턴 시각적 학습
- 그래프/트리 자료구조에 대한 이해 증진
- 알고리즘의 시간 복잡도와 공간 복잡도 개념 학습

## ✨ 주요 기능
- 🌳 **그래프/트리 생성**: 사용자 정의 그래프 생성 및 편집
- 🔍 **DFS 시각화**: 깊이 우선 탐색 과정을 단계별로 시각화
- 🔎 **BFS 시각화**: 너비 우선 탐색 과정을 단계별로 시각화
- ⏯️ **애니메이션 제어**: 재생, 일시정지, 단계별 실행
- 📊 **통계 표시**: 방문 순서, 탐색 깊이, 실행 시간 등
- 💾 **그래프 저장/로드**: 그래프 구조 저장 및 불러오기

## 🛠️ 기술 스택
- **Python 3.8+**
- **tkinter**: GUI 인터페이스
- **matplotlib**: 그래프 시각화
- **networkx**: 그래프 자료구조 처리

## 📦 설치 방법

### 🚀 자동 설치 (추천)

#### ⚠️ Python이 설치되지 않은 경우
```cmd
# Windows 사용자 - Python 설치 상태 확인 및 가이드
install_python_first.bat

# 또는 Python 자동 설치 시도
auto_install_python.bat

# Python 설치 후 아래 단계 진행
```

#### Windows 사용자
```cmd
# 저장소 클론 후
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd algorithm-visualizer

# 자동 설치 스크립트 실행 (Python 자동 설치 기능 포함)
setup_windows.bat

# 또는 빠른 설치 (로그 최소화)
quick_setup.bat
```

#### Linux/macOS 사용자  
```bash
# 저장소 클론 후
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd algorithm-visualizer

# 자동 설치 스크립트 실행 (실행 권한 부여 후)
chmod +x setup_unix.sh
./setup_unix.sh
```

> 💡 **설치 안내**: 스크립트들이 자동으로 Python 설치 상태를 확인하고, 
> 설치되지 않은 경우 **winget**, **Chocolatey**, **Windows Store** 등 
> 다양한 방법으로 자동 설치를 시도하거나 설치 가이드를 제공합니다.

### 🎯 시나리오별 설정 방법

#### 📚 시나리오 1: 처음부터 프로젝트 생성 (강사용)

```bash
# 1. uv 설치
pip install uv

# 2. 새 프로젝트 초기화
uv init algorithm-visualizer
cd algorithm-visualizer

# 3. Python 3.11 설치 및 가상환경 생성
uv python install 3.11
uv venv --python 3.11

# 4. 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows

# 5. 의존성 추가
uv add matplotlib networkx numpy Pillow scipy dataclasses-json

# 6. 개발용 패키지 추가 (선택사항)
uv add --dev pytest black flake8 mypy

# 🔍 설치 확인
python --version  # Python 3.11.x 확인
uv pip list       # 설치된 패키지 확인
```

#### 🎓 시나리오 2: 기존 프로젝트 클론 (학생용)

```bash
# 1. uv 설치 (한 번만 실행)
pip install uv

# 2. 저장소 클론
git clone <YOUR_GITHUB_REPOSITORY_URL>
# 예: git clone https://github.com/jslee7518/algorithm-visualizer.git
cd algorithm-visualizer

# 3. Python 3.11 설치 및 가상환경 생성
uv python install 3.11
uv sync

# 🔍 설치 확인 (Windows)
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -c "import matplotlib, numpy, networkx; print('✅ 모든 패키지 정상 설치됨')"

# 🔍 설치 확인 (macOS/Linux)
.venv/bin/python --version
.venv/bin/python -c "import matplotlib, numpy, networkx; print('✅ 모든 패키지 정상 설치됨')"
```

#### 🪟 Windows 사용자 추가 안내

Windows에서 PowerShell 실행 정책 오류가 발생하는 경우:

```powershell
# 방법 1: PowerShell 실행 정책 변경 (권장)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 이후 가상환경 활성화
.venv\Scripts\activate
python main.py

# 방법 2: 가상환경 활성화 없이 직접 실행
.venv\Scripts\python.exe main.py
```

> 💡 **uv의 장점**: 
> - `uv sync`: 모든 학생이 **완전히 동일한** 환경을 한 번에 구축
> - `uv.lock` 파일로 정확한 버전 고정
> - pip보다 10-100배 빠른 설치 속도
> - 의존성 해결 속도가 매우 빠름

### 🏃‍♂️ 프로그램 실행

**Windows 사용자:**
```powershell
# 방법 1: 가상환경 활성화 후 실행 (PowerShell 실행 정책 설정 필요)
.venv\Scripts\activate
python main.py

# 방법 2: 직접 실행 (추천)
.venv\Scripts\python.exe main.py
```

**macOS/Linux 사용자:**
```bash
# 가상환경 활성화 후 실행
source .venv/bin/activate
python main.py

# 또는 직접 실행
.venv/bin/python main.py
```

## 🚀 사용 방법

### 기본 사용법
1. **그래프 생성**: 
   - '노드 추가' 버튼으로 노드 생성
   - 노드를 드래그하여 연결선 생성
   
2. **알고리즘 선택**:
   - DFS 또는 BFS 선택
   - 시작 노드 지정
   
3. **시각화 실행**:
   - '시작' 버튼 클릭
   - 속도 조절 슬라이더로 애니메이션 속도 조정

### 예제 그래프
프로그램에는 다음과 같은 예제 그래프가 포함되어 있습니다:
- 이진 트리
- 무방향 그래프
- 방향 그래프
- 미로 형태 그래프

## 📸 스크린샷
*곧 추가 예정*

## 🎓 교육 활용 방안

### 수업 계획 예시
1. **1차시**: 그래프 기본 개념과 표현 방법
2. **2차시**: DFS 알고리즘 이론과 시각화 실습
3. **3차시**: BFS 알고리즘 이론과 시각화 실습
4. **4차시**: DFS vs BFS 비교 분석 실습

### 과제 아이디어
- 특정 그래프에서 DFS/BFS 탐색 순서 예측하기
- 미로 찾기 문제를 DFS/BFS로 해결하기
- 알고리즘별 성능 비교 분석하기

## 📁 프로젝트 구조
```
algorithm-visualizer/
├── main.py              # 메인 실행 파일
├── gui/                 # GUI 관련 모듈
│   ├── __init__.py
│   ├── main_window.py   # 메인 윈도우
│   └── graph_canvas.py  # 그래프 캔버스
├── algorithms/          # 알고리즘 구현
│   ├── __init__.py
│   ├── dfs.py          # DFS 구현
│   └── bfs.py          # BFS 구현
├── utils/              # 유틸리티 함수
│   ├── __init__.py
│   └── graph_utils.py  # 그래프 유틸리티
├── examples/           # 예제 그래프
├── docs/              # 문서
├── requirements.txt   # 의존성 목록
└── README.md
```

## 🤝 기여하기
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 할일 목록
- [ ] GUI 인터페이스 구현
- [ ] DFS 알고리즘 구현 및 시각화
- [ ] BFS 알고리즘 구현 및 시각화
- [ ] 예제 그래프 추가
- [ ] 사용자 매뉴얼 작성
- [ ] 단위 테스트 추가
- [ ] 성능 최적화

## 📄 라이센스
이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📧 연락처
프로젝트 관련 문의: [your-email@example.com]

## 🙏 감사의 말
이 프로젝트는 Python 교육을 위해 제작되었으며, 학생들의 알고리즘 이해도 향상에 기여하고자 합니다.

---
*Made with ❤️ for Python Education*
