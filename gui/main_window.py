"""
메인 윈도우 GUI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import networkx as nx
from typing import Optional, Dict, List
import threading
import time
import os

from .graph_canvas import GraphCanvas
from .data_structure_widget import DataStructureWidget
from utils.graph_utils import GraphUtils
from algorithms.dfs import DFS
from algorithms.bfs import BFS


class MainWindow:
    """메인 윈도우 클래스"""
    
    def __init__(self):
        """메인 윈도우 초기화"""
        self.root = tk.Tk()
        self.root.title("Algorithm Visualizer - 탐색 알고리즘 시각화")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # 그래프 및 알고리즘 관련
        self.current_graph: Optional[nx.Graph] = None
        self.current_algorithm = None
        self.algorithm_steps: List[Dict] = []
        self.current_step = 0
        self.is_playing = False
        self.animation_speed = 1.0  # 초 단위
        
        # 선택된 노드들
        self.start_node: Optional[str] = None
        self.target_node: Optional[str] = None
        
        self.setup_ui()
        self.load_sample_graph()
    
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단 컨트롤 패널
        self.setup_control_panel(main_frame)
        
        # 중간 영역 (그래프 + 사이드바)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 그래프 캔버스
        self.setup_graph_area(content_frame)
        
        # 사이드바
        self.setup_sidebar(content_frame)
        
        # 하단 상태바
        self.setup_status_bar(main_frame)
    
    def setup_control_panel(self, parent):
        """상단 컨트롤 패널 설정"""
        control_frame = ttk.LabelFrame(parent, text="컨트롤 패널", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 컨트롤 내용과 범례를 나누는 메인 프레임
        main_control_frame = ttk.Frame(control_frame)
        main_control_frame.pack(fill=tk.X)
        
        # 왼쪽: 기존 컨트롤들
        left_frame = ttk.Frame(main_control_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 첫 번째 행: 그래프 관련
        row1 = ttk.Frame(left_frame)
        row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(row1, text="그래프:").pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row1, text="샘플 그래프", 
                  command=self.load_sample_graph).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1, text="이진 트리", 
                  command=self.load_binary_tree).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1, text="미로", 
                  command=self.load_maze_graph).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1, text="그래프 로드", 
                  command=self.load_graph).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1, text="그래프 저장", 
                  command=self.save_graph).pack(side=tk.LEFT, padx=(0, 5))
        
        # 두 번째 행: 알고리즘 및 노드 선택
        row2 = ttk.Frame(left_frame)
        row2.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(row2, text="알고리즘:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.algorithm_var = tk.StringVar(value="DFS")
        ttk.Radiobutton(row2, text="DFS", variable=self.algorithm_var, 
                       value="DFS").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(row2, text="BFS", variable=self.algorithm_var, 
                       value="BFS").pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row2, text="시작 노드:").pack(side=tk.LEFT, padx=(0, 5))
        self.start_node_var = tk.StringVar()
        self.start_combo = ttk.Combobox(row2, textvariable=self.start_node_var, 
                                       width=8, state="readonly")
        self.start_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(row2, text="목표 노드:").pack(side=tk.LEFT, padx=(0, 5))
        self.target_node_var = tk.StringVar()
        self.target_combo = ttk.Combobox(row2, textvariable=self.target_node_var, 
                                        width=8, state="readonly")
        self.target_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 세 번째 행: 애니메이션 컨트롤
        row3 = ttk.Frame(left_frame)
        row3.pack(fill=tk.X)
        
        ttk.Button(row3, text="시작", 
                  command=self.start_algorithm).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row3, text="일시정지", 
                  command=self.pause_animation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row3, text="정지", 
                  command=self.stop_algorithm).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row3, text="이전 단계", 
                  command=self.prev_step).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row3, text="다음 단계", 
                  command=self.next_step).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(row3, text="속도:").pack(side=tk.LEFT, padx=(0, 5))
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(row3, from_=0.1, to=3.0, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, length=100)
        speed_scale.pack(side=tk.LEFT, padx=(0, 5))
        self.speed_label = ttk.Label(row3, text="1.0초")
        self.speed_label.pack(side=tk.LEFT)
        
        # 속도 변경 이벤트
        speed_scale.configure(command=self.on_speed_change)
        
        # 오른쪽: 범례
        self.setup_legend_panel(main_control_frame)
    
    def setup_graph_area(self, parent):
        """그래프 영역 설정"""
        graph_frame = ttk.LabelFrame(parent, text="그래프 시각화", padding=5)
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 그래프 캔버스
        self.graph_canvas = GraphCanvas(graph_frame)
    
    def setup_sidebar(self, parent):
        """사이드바 설정"""
        sidebar = ttk.Frame(parent, width=300)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # 스택/큐 시각화 위젯 추가
        self.data_structure_widget = DataStructureWidget(sidebar)
        
        # 현재 단계 정보
        step_frame = ttk.LabelFrame(sidebar, text="현재 단계", padding=10)
        step_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.step_info = tk.Text(step_frame, height=4, wrap=tk.WORD, 
                                font=('Consolas', 9))
        step_scrollbar = ttk.Scrollbar(step_frame, orient=tk.VERTICAL, 
                                      command=self.step_info.yview)
        self.step_info.configure(yscrollcommand=step_scrollbar.set)
        
        self.step_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        step_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 통계 정보
        stats_frame = ttk.LabelFrame(sidebar, text="통계", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=6, wrap=tk.WORD, 
                                 font=('Consolas', 9))
        stats_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, 
                                       command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 방문 순서
        visit_frame = ttk.LabelFrame(sidebar, text="방문 순서", padding=10)
        visit_frame.pack(fill=tk.BOTH, expand=True)
        
        self.visit_listbox = tk.Listbox(visit_frame, font=('Consolas', 9))
        visit_scrollbar2 = ttk.Scrollbar(visit_frame, orient=tk.VERTICAL, 
                                        command=self.visit_listbox.yview)
        self.visit_listbox.configure(yscrollcommand=visit_scrollbar2.set)
        
        self.visit_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        visit_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_status_bar(self, parent):
        """하단 상태바 설정"""
        self.status_bar = ttk.Label(parent, text="준비", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def on_speed_change(self, value):
        """애니메이션 속도 변경"""
        self.animation_speed = float(value)
        self.speed_label.config(text=f"{self.animation_speed:.1f}초")
    
    def update_node_combos(self):
        """노드 콤보박스 업데이트"""
        if not self.current_graph:
            self.start_combo['values'] = []
            self.target_combo['values'] = []
            return
        
        nodes = sorted(list(self.current_graph.nodes()))
        self.start_combo['values'] = [''] + nodes
        self.target_combo['values'] = [''] + nodes
        
        # 기본값 설정
        if nodes:
            self.start_node_var.set(nodes[0])
            if len(nodes) > 1:
                self.target_node_var.set(nodes[-1])
    
    def load_sample_graph(self):
        """샘플 그래프 로드"""
        self.current_graph = GraphUtils.create_sample_graph()
        self.graph_canvas.set_graph(self.current_graph)
        self.update_node_combos()
        self.update_status("샘플 그래프가 로드되었습니다.")
        self.reset_algorithm()
    
    def load_binary_tree(self):
        """이진 트리 로드"""
        self.current_graph = GraphUtils.create_sample_tree()
        self.graph_canvas.set_graph(self.current_graph)
        self.update_node_combos()
        self.update_status("이진 트리가 로드되었습니다.")
        self.reset_algorithm()
    
    def load_maze_graph(self):
        """미로 그래프 로드"""
        self.current_graph = GraphUtils.create_maze_graph()
        self.graph_canvas.set_graph(self.current_graph)
        self.update_node_combos()
        self.update_status("미로 그래프가 로드되었습니다.")
        self.reset_algorithm()
    
    def load_graph(self):
        """그래프 파일 로드"""
        filename = filedialog.askopenfilename(
            title="그래프 파일 선택",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            graph = GraphUtils.load_graph(filename)
            if graph:
                self.current_graph = graph
                self.graph_canvas.set_graph(self.current_graph)
                self.update_node_combos()
                self.update_status(f"그래프가 로드되었습니다: {os.path.basename(filename)}")
                self.reset_algorithm()
            else:
                messagebox.showerror("오류", "그래프 파일을 로드할 수 없습니다.")
    
    def save_graph(self):
        """그래프 파일 저장"""
        if not self.current_graph:
            messagebox.showwarning("경고", "저장할 그래프가 없습니다.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="그래프 저장",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if GraphUtils.save_graph(self.current_graph, filename):
                self.update_status(f"그래프가 저장되었습니다: {os.path.basename(filename)}")
            else:
                messagebox.showerror("오류", "그래프를 저장할 수 없습니다.")
    
    def start_algorithm(self):
        """알고리즘 시작"""
        if not self.current_graph:
            messagebox.showwarning("경고", "그래프를 먼저 로드하세요.")
            return
        
        start_node = self.start_node_var.get()
        if not start_node:
            messagebox.showwarning("경고", "시작 노드를 선택하세요.")
            return
        
        target_node = self.target_node_var.get() or None
        
        # 알고리즘 초기화
        algorithm_type = self.algorithm_var.get()
        if algorithm_type == "DFS":
            self.current_algorithm = DFS(self.current_graph)
        else:  # BFS
            self.current_algorithm = BFS(self.current_graph)
        
        # 알고리즘 실행 및 단계 저장
        self.algorithm_steps = []
        try:
            for step in self.current_algorithm.search(start_node, target_node):
                if 'error' in step:
                    messagebox.showerror("오류", step['error'])
                    return
                self.algorithm_steps.append(step)
        except Exception as e:
            messagebox.showerror("오류", f"알고리즘 실행 중 오류가 발생했습니다: {e}")
            return
        
        self.current_step = 0
        self.is_playing = True
        self.update_status(f"{algorithm_type} 알고리즘이 시작되었습니다.")
        
        # 애니메이션 시작
        self.animate_algorithm()
    
    def animate_algorithm(self):
        """알고리즘 애니메이션"""
        if not self.is_playing or self.current_step >= len(self.algorithm_steps):
            self.is_playing = False
            if self.current_step >= len(self.algorithm_steps):
                self.update_status("알고리즘이 완료되었습니다.")
            return
        
        # 현재 단계 표시
        self.show_step(self.current_step)
        self.current_step += 1
        
        # 다음 단계 예약
        self.root.after(int(self.animation_speed * 1000), self.animate_algorithm)
    
    def pause_animation(self):
        """애니메이션 일시정지"""
        self.is_playing = False
        self.update_status("애니메이션이 일시정지되었습니다.")
    
    def stop_algorithm(self):
        """알고리즘 정지"""
        self.is_playing = False
        self.reset_algorithm()
        self.update_status("알고리즘이 정지되었습니다.")
    
    def prev_step(self):
        """이전 단계"""
        if self.algorithm_steps and self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
    
    def next_step(self):
        """다음 단계"""
        if self.algorithm_steps and self.current_step < len(self.algorithm_steps):
            self.show_step(self.current_step)
            self.current_step += 1
    
    def show_step(self, step_index: int):
        """특정 단계 표시"""
        if not self.algorithm_steps or step_index >= len(self.algorithm_steps):
            return
        
        step = self.algorithm_steps[step_index]
        
        # 그래프 업데이트
        self.graph_canvas.update_visualization(step)
        
        # 스택/큐 위젯 업데이트
        algorithm_type = self.algorithm_var.get()
        if algorithm_type == "DFS" and 'stack' in step:
            self.data_structure_widget.set_structure_type("stack")
            self.data_structure_widget.update_data(step['stack'])
        elif algorithm_type == "BFS" and 'queue' in step:
            self.data_structure_widget.set_structure_type("queue")
            self.data_structure_widget.update_data(step['queue'])
        
        # 단계 정보 표시
        self.update_step_info(step)
        
        # 통계 업데이트
        self.update_statistics()
        
        # 방문 순서 업데이트
        self.update_visit_order(step)
    
    def update_step_info(self, step: Dict):
        """단계 정보 업데이트"""
        self.step_info.delete(1.0, tk.END)
        
        info_text = f"단계 {step.get('step', 0)}: {step.get('action', '')}\n"
        info_text += f"메시지: {step.get('message', '')}\n"
        
        if step.get('current_node'):
            info_text += f"현재 노드: {step['current_node']}\n"
        
        if 'stack' in step:
            info_text += f"스택: {step['stack']}\n"
        elif 'queue' in step:
            info_text += f"큐: {step['queue']}\n"
        
        if step.get('found_target'):
            info_text += "🎉 목표 노드를 찾았습니다!\n"
        
        self.step_info.insert(1.0, info_text)
    
    def update_statistics(self):
        """통계 정보 업데이트"""
        if not self.current_algorithm:
            return
        
        stats = self.current_algorithm.get_statistics()
        
        self.stats_text.delete(1.0, tk.END)
        
        stats_text = f"알고리즘: {stats['algorithm']}\n"
        stats_text += f"전체 노드: {stats['total_nodes']}\n"
        stats_text += f"방문한 노드: {stats['visited_nodes']}\n"
        stats_text += f"미방문 노드: {stats['unvisited_nodes']}\n"
        stats_text += f"완료율: {stats['completion_rate']:.1f}%\n"
        stats_text += f"총 단계: {stats['total_steps']}\n"
        
        if stats['algorithm'] == 'BFS' and 'max_level' in stats:
            stats_text += f"최대 레벨: {stats['max_level']}\n"
        
        self.stats_text.insert(1.0, stats_text)
    
    def update_visit_order(self, step: Dict):
        """방문 순서 업데이트"""
        if 'visit_order' not in step:
            return
        
        self.visit_listbox.delete(0, tk.END)
        
        for i, node in enumerate(step['visit_order']):
            self.visit_listbox.insert(tk.END, f"{i+1}. {node}")
    
    def reset_algorithm(self):
        """알고리즘 상태 초기화"""
        self.current_algorithm = None
        self.algorithm_steps = []
        self.current_step = 0
        self.is_playing = False
        
        if self.current_graph:
            self.graph_canvas.reset_visualization()
            self.graph_canvas.draw_graph()
        
        # 스택/큐 위젯 초기화
        self.data_structure_widget.clear_visualization()
        
        # UI 초기화
        self.step_info.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.visit_listbox.delete(0, tk.END)
    
    def update_status(self, message: str):
        """상태바 업데이트"""
        self.status_bar.config(text=message)
    
    def on_node_selected(self, node: str):
        """노드 클릭 이벤트 처리"""
        # 간단한 노드 정보 표시
        if self.current_graph and node in self.current_graph:
            neighbors = list(self.current_graph.neighbors(node))
            message = f"선택된 노드: {node}, 인접 노드: {neighbors}"
            self.update_status(message)
    
    def setup_legend_panel(self, parent):
        """범례 패널 설정"""
        legend_frame = ttk.LabelFrame(parent, text="범례", padding=5)
        legend_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 범례 아이템들을 격자로 배치
        legend_items = [
            ("●", "#87CEEB", "기본 노드"),
            ("●", "#98FB98", "방문한 노드"),
            ("●", "#FFB6C1", "현재 노드"),
            ("━", "#FF4500", "경로 간선"),
            ("1", "#FFFF00", "방문 순서")
        ]
        
        for i, (symbol, color, text) in enumerate(legend_items):
            item_frame = ttk.Frame(legend_frame)
            if i < 3:  # 첫 번째 행
                item_frame.grid(row=0, column=i, padx=5, pady=2, sticky='w')
            else:  # 두 번째 행
                item_frame.grid(row=1, column=i-3, padx=5, pady=2, sticky='w')
            
            # 심볼/색상 라벨
            if symbol == "1":  # 방문 순서는 특별 처리
                symbol_label = tk.Label(item_frame, text=symbol, 
                                      bg=color, fg="black", 
                                      font=('Arial', 8, 'bold'),
                                      width=2, height=1, relief='raised')
            else:
                symbol_label = tk.Label(item_frame, text=symbol, 
                                      fg=color, font=('Arial', 12, 'bold'))
            symbol_label.pack(side=tk.LEFT)
            
            # 텍스트 라벨
            text_label = ttk.Label(item_frame, text=text, font=('Arial', 8))
            text_label.pack(side=tk.LEFT, padx=(2, 0))
    
    def run(self):
        """애플리케이션 실행"""
        # 창 중앙에 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop() 