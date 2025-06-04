#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo -e " Algorithm Visualizer 설치 스크립트"
echo -e " Linux/macOS 버전"
echo -e "==========================================${NC}"
echo

# 에러 발생 시 스크립트 종료 (Python 체크는 예외)
# set -e는 나중에 설정

# 에러 핸들링 함수
handle_error() {
    echo -e "${RED}❌ 오류가 발생했습니다: $1${NC}"
    exit 1
}

# Python 설치 가이드 함수
show_python_install_guide() {
    echo -e "${RED}❌ Python이 설치되지 않았습니다!${NC}"
    echo
    echo -e "${BLUE}📋 Python 설치 방법:${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo -e "${YELLOW}macOS 사용자:${NC}"
        echo "  1. Homebrew 사용: brew install python"
        echo "  2. 공식 사이트: https://www.python.org/downloads/"
        echo "  3. pyenv 사용: brew install pyenv && pyenv install 3.11"
    else
        # Linux
        echo -e "${YELLOW}Linux 사용자:${NC}"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
    fi
    
    echo
    echo -e "${BLUE}설치 완료 후 이 스크립트를 다시 실행해주세요.${NC}"
    exit 1
}

echo -e "${YELLOW}[0/6] Python 설치 확인 중...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3이 설치되어 있습니다.${NC}"
    python3 --version
elif command -v python &> /dev/null; then
    echo -e "${GREEN}✅ Python이 설치되어 있습니다.${NC}"
    python --version
else
    show_python_install_guide
fi

# 이제부터 에러 발생 시 스크립트 종료
set -e

echo
echo -e "${YELLOW}[1/6] uv 설치 확인 중...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✅ uv가 이미 설치되어 있습니다.${NC}"
else
    echo "uv가 설치되지 않았습니다. 설치 중..."
    
    # 여러 방법으로 uv 설치 시도
    install_success=false
    
    # 방법 1: pip 사용
    if command -v pip3 &> /dev/null; then
        echo "pip3를 사용하여 uv 설치 시도 중..."
        if pip3 install uv 2>/dev/null; then
            install_success=true
        fi
    elif command -v pip &> /dev/null; then
        echo "pip을 사용하여 uv 설치 시도 중..."
        if pip install uv 2>/dev/null; then
            install_success=true
        fi
    fi
    
    # 방법 2: curl 사용
    if [ "$install_success" = false ]; then
        echo "curl을 사용하여 uv 설치 시도 중..."
        if curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null; then
            export PATH="$HOME/.local/bin:$PATH"
            install_success=true
        fi
    fi
    
    # 방법 3: macOS Homebrew
    if [ "$install_success" = false ] && [[ "$OSTYPE" == "darwin"* ]] && command -v brew &> /dev/null; then
        echo "Homebrew를 사용하여 uv 설치 시도 중..."
        if brew install uv 2>/dev/null; then
            install_success=true
        fi
    fi
    
    if [ "$install_success" = false ]; then
        handle_error "uv 설치 실패. https://docs.astral.sh/uv/getting-started/installation/ 참조"
    fi
    
    echo -e "${GREEN}✅ uv 설치 완료${NC}"
fi

echo
echo -e "${YELLOW}[2/6] Python 3.11 설치 중...${NC}"
uv python install 3.11 || handle_error "Python 3.11 설치 실패"
echo -e "${GREEN}✅ Python 3.11 설치 완료${NC}"

echo
echo -e "${YELLOW}[3/6] 가상환경 생성 및 의존성 설치 중...${NC}"
uv sync || handle_error "가상환경 생성 또는 의존성 설치 실패"
echo -e "${GREEN}✅ 가상환경 및 의존성 설치 완료${NC}"

echo
echo -e "${YELLOW}[4/6] 설치 확인 중...${NC}"
.venv/bin/python --version || handle_error "Python 버전 확인 실패"
.venv/bin/python -c "import matplotlib, numpy, networkx; print('✅ 모든 패키지 정상 설치됨')" || handle_error "패키지 설치 확인 실패"

echo
echo -e "${YELLOW}[5/6] 설치 완료!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo
echo -e "${GREEN}🎉 설치가 성공적으로 완료되었습니다!${NC}"
echo
echo -e "${BLUE}📋 프로그램 실행 방법:${NC}"
echo -e "   방법 1: ${YELLOW}.venv/bin/python main.py${NC}"
echo -e "   방법 2: ${YELLOW}source .venv/bin/activate${NC} 후 ${YELLOW}python main.py${NC}"
echo
echo -e "${BLUE}📝 추가 명령어:${NC}"
echo -e "   가상환경 활성화: ${YELLOW}source .venv/bin/activate${NC}"
echo -e "   가상환경 비활성화: ${YELLOW}deactivate${NC}"
echo
echo -e "${BLUE}==========================================${NC}"
echo 