"""
스택/큐 시각화 위젯
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DataStructureWidget:
    """스택과 큐를 시각적으로 표현하는 위젯"""
    
    def __init__(self, parent):
        """
        위젯 초기화
        
        Args:
            parent: 부모 위젯
        """
        self.parent = parent
        self.current_structure = "stack"  # "stack" 또는 "queue"
        self.data = []
        
        # 색상 설정
        self.colors = {
            'stack_bg': '#E6F3FF',      # 연한 파란색
            'queue_bg': '#F0FFF0',      # 연한 초록색
            'item_color': '#87CEEB',    # 스카이블루
            'item_border': '#4682B4',   # 스틸블루
            'arrow_color': '#FF6347',   # 토마토색
            'text_color': '#000000'     # 검은색
        }
        
        self.setup_widget()
    
    def setup_widget(self):
        """위젯 설정"""
        # 메인 프레임
        self.main_frame = ttk.LabelFrame(self.parent, text="스택/큐 시각화", padding=5)
        self.main_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 상단: 타입 표시
        self.type_frame = ttk.Frame(self.main_frame)
        self.type_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.type_label = ttk.Label(self.type_frame, text="현재: 없음", 
                                   font=('Arial', 10, 'bold'))
        self.type_label.pack()
        
        # matplotlib 캔버스
        self.fig = Figure(figsize=(4, 3), dpi=80, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 초기 상태
        self.clear_visualization()
    
    def set_structure_type(self, structure_type: str):
        """
        데이터 구조 타입 설정
        
        Args:
            structure_type: "stack" 또는 "queue"
        """
        self.current_structure = structure_type
        if structure_type == "stack":
            self.type_label.config(text="현재: 스택 (LIFO)")
        elif structure_type == "queue":
            self.type_label.config(text="현재: 큐 (FIFO)")
        else:
            self.type_label.config(text="현재: 없음")
    
    def update_data(self, data: List[str]):
        """
        데이터 업데이트 및 시각화
        
        Args:
            data: 표시할 데이터 리스트
        """
        self.data = data.copy() if data else []
        self.draw_visualization()
    
    def draw_visualization(self):
        """시각화 그리기"""
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.axis('off')
        
        if not self.data:
            self.ax.text(5, 4, '비어있음', ha='center', va='center', 
                        fontsize=12, color='gray')
            self.canvas.draw()
            return
        
        if self.current_structure == "stack":
            self.draw_stack()
        elif self.current_structure == "queue":
            self.draw_queue()
        
        self.canvas.draw()
    
    def draw_stack(self):
        """스택 시각화 그리기"""
        if not self.data:
            return
        
        # 배경
        self.ax.add_patch(plt.Rectangle((3, 1), 4, 6, 
                                       facecolor=self.colors['stack_bg'], 
                                       alpha=0.3))
        
        # 스택 아이템들 (아래부터 위로)
        box_height = 0.8
        max_items = min(len(self.data), 6)  # 최대 6개까지 표시
        
        for i in range(max_items):
            y_pos = 1.5 + i * (box_height + 0.1)
            
            # 박스 그리기
            self.ax.add_patch(plt.Rectangle((3.5, y_pos), 3, box_height,
                                           facecolor=self.colors['item_color'],
                                           edgecolor=self.colors['item_border'],
                                           linewidth=2))
            
            # 텍스트
            item_text = self.data[-(i+1)]  # 스택은 뒤에서부터 (top부터)
            self.ax.text(5, y_pos + box_height/2, item_text, 
                        ha='center', va='center', fontsize=10, fontweight='bold')
        
        # TOP 표시
        if self.data:
            top_y = 1.5 + (max_items-1) * (box_height + 0.1) + box_height
            self.ax.annotate('TOP', xy=(6.5, top_y), xytext=(8, top_y),
                            arrowprops=dict(arrowstyle='->', color=self.colors['arrow_color'], lw=2),
                            fontsize=10, fontweight='bold', color=self.colors['arrow_color'])
        
        # 스택이 6개보다 많을 때
        if len(self.data) > 6:
            self.ax.text(5, 7.5, f'... (+{len(self.data)-6}개)', 
                        ha='center', va='center', fontsize=8, style='italic')
    
    def draw_queue(self):
        """큐 시각화 그리기"""
        if not self.data:
            return
        
        # 배경
        self.ax.add_patch(plt.Rectangle((0.5, 3), 9, 2, 
                                       facecolor=self.colors['queue_bg'], 
                                       alpha=0.3))
        
        # 큐 아이템들 (왼쪽부터 오른쪽으로)
        box_width = 1.2
        max_items = min(len(self.data), 6)  # 최대 6개까지 표시
        
        for i in range(max_items):
            x_pos = 1 + i * (box_width + 0.1)
            
            # 박스 그리기
            self.ax.add_patch(plt.Rectangle((x_pos, 3.5), box_width, 1,
                                           facecolor=self.colors['item_color'],
                                           edgecolor=self.colors['item_border'],
                                           linewidth=2))
            
            # 텍스트
            item_text = self.data[i]  # 큐는 앞에서부터 (front부터)
            self.ax.text(x_pos + box_width/2, 4, item_text, 
                        ha='center', va='center', fontsize=10, fontweight='bold')
        
        # FRONT 표시
        if self.data:
            self.ax.annotate('FRONT', xy=(1, 3.2), xytext=(1, 2.5),
                            arrowprops=dict(arrowstyle='->', color=self.colors['arrow_color'], lw=2),
                            fontsize=10, fontweight='bold', color=self.colors['arrow_color'])
        
        # REAR 표시
        if self.data:
            rear_x = 1 + (max_items-1) * (box_width + 0.1) + box_width
            self.ax.annotate('REAR', xy=(rear_x, 5.8), xytext=(rear_x, 6.5),
                            arrowprops=dict(arrowstyle='->', color=self.colors['arrow_color'], lw=2),
                            fontsize=10, fontweight='bold', color=self.colors['arrow_color'])
        
        # 큐가 6개보다 많을 때
        if len(self.data) > 6:
            self.ax.text(8.5, 3, f'... (+{len(self.data)-6}개)', 
                        ha='center', va='center', fontsize=8, style='italic')
    
    def clear_visualization(self):
        """시각화 초기화"""
        self.data = []
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.axis('off')
        self.ax.text(5, 4, '알고리즘을 시작하세요', ha='center', va='center', 
                    fontsize=12, color='gray')
        self.canvas.draw()
    
    def highlight_operation(self, operation: str, item: Optional[str] = None):
        """
        특정 연산 강조 표시
        
        Args:
            operation: "push", "pop", "enqueue", "dequeue"
            item: 연산 대상 아이템
        """
        # 기본 시각화 먼저 그리기
        self.draw_visualization()
        
        # 연산별 강조 효과 추가
        if operation == "push" and item and self.current_structure == "stack":
            # 새로 추가될 아이템을 점선으로 표시
            max_items = min(len(self.data), 6)
            y_pos = 1.5 + max_items * 0.9
            self.ax.add_patch(plt.Rectangle((3.5, y_pos), 3, 0.8,
                                           facecolor='yellow', alpha=0.5,
                                           edgecolor='red', linewidth=2, linestyle='--'))
            self.ax.text(5, y_pos + 0.4, item, ha='center', va='center', 
                        fontsize=10, fontweight='bold', color='red')
        
        elif operation == "enqueue" and item and self.current_structure == "queue":
            # 새로 추가될 아이템을 점선으로 표시
            max_items = min(len(self.data), 6)
            x_pos = 1 + max_items * 1.3
            self.ax.add_patch(plt.Rectangle((x_pos, 3.5), 1.2, 1,
                                           facecolor='yellow', alpha=0.5,
                                           edgecolor='red', linewidth=2, linestyle='--'))
            self.ax.text(x_pos + 0.6, 4, item, ha='center', va='center', 
                        fontsize=10, fontweight='bold', color='red')
        
        self.canvas.draw() 