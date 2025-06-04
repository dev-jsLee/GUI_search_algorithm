"""
그래프 시각화 캔버스
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional, Set


class GraphCanvas:
    """그래프 시각화를 위한 matplotlib 캔버스 클래스"""
    
    def __init__(self, parent):
        """
        그래프 캔버스 초기화
        
        Args:
            parent: 부모 위젯
        """
        self.parent = parent
        self.graph: Optional[nx.Graph] = None
        self.positions: Dict[str, Tuple[float, float]] = {}
        
        # 시각화 상태
        self.visited_nodes: Set[str] = set()
        self.current_node: Optional[str] = None
        self.path_edges: List[Tuple[str, str]] = []
        self.highlighted_nodes: Set[str] = set()
        self.visit_order: List[str] = []  # 방문 순서 리스트 추가
        
        # 색상 설정
        self.colors = {
            'default_node': '#87CEEB',      # 기본 노드 (연한 파란색)
            'visited_node': '#98FB98',      # 방문한 노드 (연한 초록색)
            'current_node': '#FFB6C1',     # 현재 노드 (연한 분홍색)
            'target_node': '#FF6347',      # 목표 노드 (토마토색)
            'highlighted_node': '#FFD700', # 강조된 노드 (금색)
            'default_edge': '#CCCCCC',     # 기본 간선 (회색)
            'path_edge': '#FF4500',        # 경로 간선 (주황색)
            'tree_edge': '#32CD32'         # 트리 간선 (연한 녹색)
        }
        
        self.setup_canvas()
    
    def setup_canvas(self):
        """matplotlib 캔버스 설정"""
        # Figure 생성
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        # 캔버스 생성
        self.canvas = FigureCanvasTkAgg(self.fig, self.parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 초기 설정
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_title('그래프 시각화', fontsize=14, fontweight='bold', pad=20)
        
        # 마우스 이벤트 연결
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        # 초기 빈 그래프 표시
        self.clear_graph()
    
    def set_graph(self, graph: nx.Graph):
        """
        그래프 설정
        
        Args:
            graph: NetworkX 그래프
        """
        self.graph = graph.copy()
        
        # 노드 위치 설정
        self.positions = {}
        for node, data in self.graph.nodes(data=True):
            if 'pos' in data:
                self.positions[node] = data['pos']
        
        # 위치가 없는 노드들은 spring layout으로 배치
        nodes_without_pos = [node for node in self.graph.nodes() if node not in self.positions]
        if nodes_without_pos:
            pos_layout = nx.spring_layout(self.graph.subgraph(nodes_without_pos), k=1, iterations=50)
            self.positions.update(pos_layout)
        
        self.reset_visualization()
        self.draw_graph()
    
    def reset_visualization(self):
        """시각화 상태 초기화"""
        self.visited_nodes.clear()
        self.current_node = None
        self.path_edges.clear()
        self.highlighted_nodes.clear()
        self.visit_order.clear()  # 방문 순서 리스트도 초기화
    
    def update_visualization(self, step_info: Dict):
        """
        알고리즘 단계에 따라 시각화 업데이트
        
        Args:
            step_info: 알고리즘 단계 정보
        """
        if not self.graph:
            return
        
        # 상태 업데이트
        if 'visited' in step_info:
            self.visited_nodes = step_info['visited']
        
        if 'current_node' in step_info:
            self.current_node = step_info['current_node']
        
        # 방문 순서 업데이트 (중요!)
        if 'visit_order' in step_info:
            self.visit_order = step_info['visit_order'].copy()
        
        # 그래프 다시 그리기
        self.draw_graph()
    
    def draw_graph(self):
        """그래프 그리기"""
        if not self.graph:
            self.clear_graph()
            return
        
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_title('그래프 시각화', fontsize=14, fontweight='bold', pad=20)
        
        if not self.positions:
            return
        
        # 간선 그리기
        self.draw_edges()
        
        # 노드 그리기
        self.draw_nodes()
        
        # 범례는 컨트롤 패널로 이동했으므로 제거
        # self.add_legend()
        
        # 캔버스 업데이트
        self.canvas.draw()
    
    def draw_edges(self):
        """간선 그리기"""
        if not self.graph.edges():
            return
        
        # 기본 간선
        edge_colors = []
        for edge in self.graph.edges():
            if edge in self.path_edges or (edge[1], edge[0]) in self.path_edges:
                edge_colors.append(self.colors['path_edge'])
            else:
                edge_colors.append(self.colors['default_edge'])
        
        nx.draw_networkx_edges(
            self.graph,
            self.positions,
            ax=self.ax,
            edge_color=edge_colors,
            width=2.0,
            alpha=0.7
        )
    
    def draw_nodes(self):
        """노드 그리기"""
        if not self.graph.nodes():
            return
        
        # 노드 색상 결정
        node_colors = []
        for node in self.graph.nodes():
            if node == self.current_node:
                node_colors.append(self.colors['current_node'])
            elif node in self.highlighted_nodes:
                node_colors.append(self.colors['highlighted_node'])
            elif node in self.visited_nodes:
                node_colors.append(self.colors['visited_node'])
            else:
                node_colors.append(self.colors['default_node'])
        
        # 노드 그리기
        nx.draw_networkx_nodes(
            self.graph,
            self.positions,
            ax=self.ax,
            node_color=node_colors,
            node_size=800,
            alpha=0.9,
            edgecolors='black',
            linewidths=2
        )
        
        # 노드 레이블 그리기
        labels = {}
        for node, data in self.graph.nodes(data=True):
            labels[node] = data.get('label', str(node))
        
        nx.draw_networkx_labels(
            self.graph,
            self.positions,
            labels,
            ax=self.ax,
            font_size=12,
            font_weight='bold',
            font_color='black'
        )
        
        # 방문 순서 표시
        for i, node in enumerate(self.visit_order):
            if node in self.positions:
                x, y = self.positions[node]
                self.ax.annotate(
                    str(i + 1),
                    (x, y),
                    xytext=(15, 15),
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    fontsize=10,
                    fontweight='bold'
                )
    
    def highlight_path(self, path: List[str]):
        """
        경로 강조 표시
        
        Args:
            path: 강조할 경로 (노드 리스트)
        """
        self.path_edges.clear()
        
        if len(path) > 1:
            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1])
                if self.graph.has_edge(edge[0], edge[1]):
                    self.path_edges.append(edge)
        
        self.draw_graph()
    
    def highlight_nodes(self, nodes: List[str]):
        """
        노드들 강조 표시
        
        Args:
            nodes: 강조할 노드 리스트
        """
        self.highlighted_nodes = set(nodes)
        self.draw_graph()
    
    def clear_highlights(self):
        """모든 강조 표시 제거"""
        self.path_edges.clear()
        self.highlighted_nodes.clear()
        self.draw_graph()
    
    def clear_graph(self):
        """그래프 지우기"""
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, '그래프를 로드하세요', 
                    transform=self.ax.transAxes, 
                    ha='center', va='center',
                    fontsize=16, color='gray')
        self.canvas.draw()
    
    def on_click(self, event):
        """마우스 클릭 이벤트 처리"""
        if event.inaxes != self.ax or not self.graph:
            return
        
        # 클릭한 위치와 가장 가까운 노드 찾기
        clicked_x, clicked_y = event.xdata, event.ydata
        if clicked_x is None or clicked_y is None:
            return
        
        min_distance = float('inf')
        closest_node = None
        
        for node, (x, y) in self.positions.items():
            distance = np.sqrt((x - clicked_x)**2 + (y - clicked_y)**2)
            if distance < min_distance:
                min_distance = distance
                closest_node = node
        
        # 클릭한 위치가 노드에 충분히 가까운 경우
        if min_distance < 0.1:  # 임계값
            self.on_node_click(closest_node)
    
    def on_node_click(self, node: str):
        """
        노드 클릭 이벤트 처리
        
        Args:
            node: 클릭된 노드
        """
        # 부모 윈도우에 노드 클릭 이벤트 전달
        if hasattr(self.parent, 'on_node_selected'):
            self.parent.on_node_selected(node)
    
    def save_image(self, filename: str):
        """
        현재 그래프 이미지 저장
        
        Args:
            filename: 저장할 파일명
        """
        try:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
            return True
        except Exception as e:
            print(f"이미지 저장 실패: {e}")
            return False
    
    def set_node_positions(self, positions: Dict[str, Tuple[float, float]]):
        """
        노드 위치 설정
        
        Args:
            positions: 노드별 위치 딕셔너리
        """
        self.positions = positions.copy()
        if self.graph:
            for node, pos in positions.items():
                if node in self.graph:
                    self.graph.nodes[node]['pos'] = pos
        self.draw_graph()
    
    def get_graph_bounds(self) -> Tuple[float, float, float, float]:
        """
        그래프의 경계 반환
        
        Returns:
            (min_x, max_x, min_y, max_y)
        """
        if not self.positions:
            return (0, 1, 0, 1)
        
        x_coords = [pos[0] for pos in self.positions.values()]
        y_coords = [pos[1] for pos in self.positions.values()]
        
        return (min(x_coords), max(x_coords), min(y_coords), max(y_coords)) 