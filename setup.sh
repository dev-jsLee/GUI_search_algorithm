#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo -e " Algorithm Visualizer 설치"
echo -e " 한 번의 명령으로 모든 설정 완료!"
echo -e "==========================================${NC}"
echo

# Python 설치 상태 및 버전 확인
echo -e "${YELLOW}🔍 Python 설치 상태 확인 중...${NC}"

PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"  
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
else
    echo -e "${RED}❌ Python이 설치되지 않았습니다.${NC}"
    echo
    echo -e "${BLUE}🤖 Python을 자동으로 설치하시겠습니까? (Y/N)${NC}"
    read -p "선택: " choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo
        echo -e "${YELLOW}🚀 Python 자동 설치를 시작합니다...${NC}"
        chmod +x scripts/setup_unix.sh
        ./scripts/setup_unix.sh
        exit $?
    else
        echo
        echo -e "${BLUE}📋 Python 설치 안내를 표시합니다...${NC}"
        chmod +x scripts/setup_unix.sh
        ./scripts/setup_unix.sh
        exit 1
    fi
fi

echo -e "${GREEN}✅ Python이 설치되어 있습니다.${NC}"
echo "현재 버전: $PYTHON_VERSION"

# Python 3.11 버전 확인
if [[ "$PYTHON_VERSION" == 3.11* ]]; then
    echo -e "${GREEN}✅ Python 3.11 버전이 확인되었습니다!${NC}"
else
    echo
    echo -e "${YELLOW}⚠️ Python $PYTHON_VERSION이 설치되어 있지만, 3.11 버전이 아닙니다.${NC}"
    echo
    echo -e "${BLUE}🔄 Python 3.11을 추가로 설치하고 가상환경을 구성하시겠습니까? (Y/N)${NC}"
    read -p "선택: " choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo
        echo -e "${YELLOW}🚀 Python 3.11 설치 및 프로젝트 설정을 진행합니다...${NC}"
        chmod +x scripts/setup_unix.sh
        ./scripts/setup_unix.sh
        exit $?
    else
        echo
        echo -e "${BLUE}ℹ️ 기존 Python 버전으로 설치를 진행합니다.${NC}"
        echo "  (일부 기능이 정상 동작하지 않을 수 있습니다)"
    fi
fi

echo
echo -e "${YELLOW}🎯 가상환경 생성 및 의존성 설치를 시작합니다...${NC}"
echo

# uv 설치 확인 및 설치
echo -e "${YELLOW}[1/4] uv 설치 확인 중...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✅ uv가 이미 설치되어 있습니다${NC}"
else
    echo "uv 설치 중..."
    
    # pip으로 설치 시도
    if command -v pip3 &> /dev/null; then
        pip3 install uv >/dev/null 2>&1
    elif command -v pip &> /dev/null; then
        pip install uv >/dev/null 2>&1
    else
        # curl로 설치 시도
        curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    if command -v uv &> /dev/null; then
        echo -e "${GREEN}✅ uv 설치 완료${NC}"
    else
        echo -e "${RED}❌ uv 설치 실패! 인터넷 연결을 확인해주세요.${NC}"
        exit 1
    fi
fi

echo
echo -e "${YELLOW}[2/4] Python 3.11 확인 중...${NC}"
if uv python install 3.11 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Python 3.11 준비 완료${NC}"
else
    echo -e "${YELLOW}⚠️ Python 3.11 설치 중 문제가 발생했습니다. 기존 Python으로 진행합니다.${NC}"
fi

echo
echo -e "${YELLOW}[3/4] 가상환경 생성 및 패키지 설치 중...${NC}"
if uv sync >/dev/null 2>&1; then
    echo -e "${GREEN}✅ 가상환경 및 패키지 설치 완료${NC}"
else
    echo -e "${RED}❌ 가상환경 생성 실패!${NC}"
    echo "상세한 로그를 확인하려면 scripts/setup_unix.sh를 실행해주세요."
    exit 1
fi

echo
echo -e "${YELLOW}[4/4] 설치 확인 중...${NC}"
if .venv/bin/python --version >/dev/null 2>&1; then
    if .venv/bin/python -c "import matplotlib, numpy, networkx; print('패키지 확인 완료!')" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ 모든 패키지 설치 확인 완료!${NC}"
    else
        echo -e "${YELLOW}⚠️ 일부 패키지가 누락되었을 수 있습니다.${NC}"
    fi
else
    echo -e "${RED}❌ 가상환경 확인 실패!${NC}"
    exit 1
fi

echo
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}🎉 설치가 완료되었습니다!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo
echo -e "${BLUE}📋 프로그램 실행 방법:${NC}"
echo -e "   ${YELLOW}.venv/bin/python main.py${NC}"
echo
echo -e "${BLUE}📂 추가 스크립트:${NC}"
echo -e "   scripts/ 폴더에서 개별 설치 스크립트 확인 가능"
echo 