"""
matplotlib 한글 폰트 설정 유틸리티
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import warnings
import os


class FontUtils:
    """matplotlib 한글 폰트 설정을 위한 유틸리티 클래스"""
    
    @staticmethod
    def setup_korean_font():
        """
        시스템에 맞는 한글 폰트를 자동으로 설정
        Windows: 맑은 고딕, macOS: Apple SD Gothic Neo, Linux: Noto Sans CJK
        """
        try:
            system = platform.system()
            
            # 시스템별 기본 한글 폰트 설정
            font_candidates = []
            
            if system == "Windows":
                font_candidates = [
                    "Malgun Gothic",  # 맑은 고딕
                    "Microsoft YaHei",
                    "SimHei",
                    "Gulim",  # 굴림
                    "Dotum"   # 돋움
                ]
            elif system == "Darwin":  # macOS
                font_candidates = [
                    "Apple SD Gothic Neo",
                    "AppleGothic",
                    "Helvetica"
                ]
            else:  # Linux
                font_candidates = [
                    "Noto Sans CJK KR",
                    "Noto Sans CJK",
                    "DejaVu Sans",
                    "Liberation Sans"
                ]
            
            # 사용 가능한 폰트 찾기
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            selected_font = None
            
            for font in font_candidates:
                if font in available_fonts:
                    selected_font = font
                    break
            
            if selected_font:
                # matplotlib 폰트 설정
                plt.rcParams['font.family'] = selected_font
                plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
                
                print(f"✅ 한글 폰트 설정 완료: {selected_font}")
                return True
            else:
                # 기본 폰트로 fallback
                FontUtils._setup_fallback_font()
                return False
                
        except Exception as e:
            print(f"⚠️ 폰트 설정 중 오류 발생: {e}")
            FontUtils._setup_fallback_font()
            return False
    
    @staticmethod
    def _setup_fallback_font():
        """폰트 설정이 실패했을 때 기본 설정"""
        try:
            # 기본 설정으로 fallback
            plt.rcParams['axes.unicode_minus'] = False
            
            # 가능한 한글 폰트 목록에서 검색
            font_list = [f.name for f in fm.fontManager.ttflist]
            korean_fonts = [f for f in font_list if any(keyword in f.lower() for keyword in 
                          ['gothic', 'malgun', 'gulim', 'dotum', 'noto', 'apple'])]
            
            if korean_fonts:
                plt.rcParams['font.family'] = korean_fonts[0]
                print(f"📝 대체 폰트 사용: {korean_fonts[0]}")
            else:
                print("⚠️ 한글 폰트를 찾을 수 없습니다. 영문으로 표시됩니다.")
                
        except Exception as e:
            print(f"⚠️ 대체 폰트 설정 실패: {e}")
    
    @staticmethod
    def get_available_korean_fonts():
        """시스템에서 사용 가능한 한글 폰트 목록 반환"""
        try:
            font_list = [f.name for f in fm.fontManager.ttflist]
            
            # 한글 폰트로 추정되는 폰트들 필터링
            korean_keywords = ['gothic', 'malgun', 'gulim', 'dotum', 'batang', 
                             'gungsuh', 'noto', 'apple', 'nanum', 'spoqa']
            
            korean_fonts = []
            for font in font_list:
                if any(keyword in font.lower() for keyword in korean_keywords):
                    korean_fonts.append(font)
            
            return sorted(list(set(korean_fonts)))
            
        except Exception as e:
            print(f"한글 폰트 목록 조회 실패: {e}")
            return []
    
    @staticmethod
    def test_korean_display():
        """한글 표시 테스트"""
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, '한글 테스트\n깊이 우선 탐색 (DFS)\n너비 우선 탐색 (BFS)', 
                   ha='center', va='center', fontsize=14)
            ax.set_title('한글 폰트 테스트')
            ax.axis('off')
            
            return fig
            
        except Exception as e:
            print(f"한글 표시 테스트 실패: {e}")
            return None
    
    @staticmethod
    def print_font_info():
        """현재 폰트 설정 정보 출력"""
        try:
            current_font = plt.rcParams['font.family']
            unicode_minus = plt.rcParams['axes.unicode_minus']
            
            print("=" * 40)
            print("📋 현재 matplotlib 폰트 설정")
            print("=" * 40)
            print(f"폰트 패밀리: {current_font}")
            print(f"유니코드 마이너스: {unicode_minus}")
            print(f"플랫폼: {platform.system()}")
            
            available_korean = FontUtils.get_available_korean_fonts()
            if available_korean:
                print(f"사용 가능한 한글 폰트: {len(available_korean)}개")
                for font in available_korean[:5]:  # 상위 5개만 표시
                    print(f"  - {font}")
                if len(available_korean) > 5:
                    print(f"  ... 외 {len(available_korean) - 5}개")
            else:
                print("사용 가능한 한글 폰트: 없음")
            print("=" * 40)
            
        except Exception as e:
            print(f"폰트 정보 출력 실패: {e}") 