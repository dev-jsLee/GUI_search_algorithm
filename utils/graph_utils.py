"""
그래프 유틸리티 클래스
"""

import networkx as nx
import json
import os
from typing import Dict, List, Tuple, Optional


class GraphUtils:
    """그래프 생성, 조작, 저장/로드를 위한 유틸리티 클래스"""
    
    @staticmethod
    def create_empty_graph() -> nx.Graph:
        """빈 그래프 생성"""
        return nx.Graph()
    
    @staticmethod
    def create_sample_tree() -> nx.Graph:
        """샘플 이진 트리 생성"""
        G = nx.Graph()
        
        # 노드 추가 (레벨별로 배치) - 노드 ID를 문자열로 통일
        nodes = [
            ('1', {'pos': (0, 2), 'label': '1'}),
            ('2', {'pos': (-1, 1), 'label': '2'}),
            ('3', {'pos': (1, 1), 'label': '3'}),
            ('4', {'pos': (-1.5, 0), 'label': '4'}),
            ('5', {'pos': (-0.5, 0), 'label': '5'}),
            ('6', {'pos': (0.5, 0), 'label': '6'}),
            ('7', {'pos': (1.5, 0), 'label': '7'})
        ]
        
        G.add_nodes_from(nodes)
        
        # 간선 추가 - 간선도 문자열로 통일
        edges = [('1', '2'), ('1', '3'), ('2', '4'), ('2', '5'), ('3', '6'), ('3', '7')]
        G.add_edges_from(edges)
        
        return G
    
    @staticmethod
    def create_sample_graph() -> nx.Graph:
        """샘플 무방향 그래프 생성"""
        G = nx.Graph()
        
        # 노드 추가
        nodes = [
            ('A', {'pos': (0, 2), 'label': 'A'}),
            ('B', {'pos': (-1, 1), 'label': 'B'}),
            ('C', {'pos': (1, 1), 'label': 'C'}),
            ('D', {'pos': (-2, 0), 'label': 'D'}),
            ('E', {'pos': (0, 0), 'label': 'E'}),
            ('F', {'pos': (2, 0), 'label': 'F'})
        ]
        
        G.add_nodes_from(nodes)
        
        # 간선 추가
        edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), 
                ('C', 'E'), ('C', 'F'), ('D', 'E'), ('E', 'F')]
        G.add_edges_from(edges)
        
        return G
    
    @staticmethod
    def create_maze_graph() -> nx.Graph:
        """미로 형태 그래프 생성 - 모든 노드가 연결되도록 설계"""
        G = nx.Graph()
        
        # 4x4 격자 미로
        nodes = []
        for i in range(4):
            for j in range(4):
                node_id = f"{i}_{j}"
                pos = (j, 3-i)  # (x, y) 좌표
                nodes.append((node_id, {'pos': pos, 'label': node_id}))
        
        G.add_nodes_from(nodes)
        
        # 연결된 미로 간선 설계 (시작점 0_0에서 목표점 3_3까지 경로 보장)
        # 미로 형태이면서도 모든 노드가 연결되도록 설계
        edges = [
            # 첫 번째 행 (0_x)
            ('0_0', '0_1'), ('0_1', '0_2'), ('0_2', '0_3'),
            
            # 세로 연결
            ('0_0', '1_0'),  # 시작점에서 아래로
            ('0_3', '1_3'),  # 첫 번째 행 끝에서 아래로
            
            # 두 번째 행 (1_x)
            ('1_0', '1_1'), ('1_2', '1_3'),
            ('1_1', '2_1'),  # 아래로 연결
            ('1_2', '2_2'),  # 아래로 연결
            
            # 세 번째 행 (2_x)
            ('2_0', '2_1'), ('2_1', '2_2'), ('2_2', '2_3'),
            ('1_0', '2_0'),  # 위에서 아래로
            ('2_3', '3_3'),  # 목표점으로 연결
            
            # 네 번째 행 (3_x)
            ('3_0', '3_1'), ('3_1', '3_2'), ('3_2', '3_3'),
            ('2_0', '3_0'),  # 위에서 아래로
            
            # 추가 연결로 경로 다양성 확보
            ('0_2', '1_2'),  # 위에서 아래로 추가 경로
            ('1_1', '1_2'),  # 가로 연결 추가
        ]
        G.add_edges_from(edges)
        
        return G
    
    @staticmethod
    def add_node(graph: nx.Graph, node_id: str, pos: Tuple[float, float], 
                 label: Optional[str] = None) -> bool:
        """노드 추가"""
        try:
            if node_id in graph:
                return False  # 이미 존재하는 노드
            
            graph.add_node(node_id, pos=pos, label=label or node_id)
            return True
        except Exception:
            return False
    
    @staticmethod
    def add_edge(graph: nx.Graph, node1: str, node2: str) -> bool:
        """간선 추가"""
        try:
            if not graph.has_node(node1) or not graph.has_node(node2):
                return False  # 노드가 존재하지 않음
            
            if graph.has_edge(node1, node2):
                return False  # 이미 존재하는 간선
            
            graph.add_edge(node1, node2)
            return True
        except Exception:
            return False
    
    @staticmethod
    def remove_node(graph: nx.Graph, node_id: str) -> bool:
        """노드 제거"""
        try:
            if node_id not in graph:
                return False
            
            graph.remove_node(node_id)
            return True
        except Exception:
            return False
    
    @staticmethod
    def remove_edge(graph: nx.Graph, node1: str, node2: str) -> bool:
        """간선 제거"""
        try:
            if not graph.has_edge(node1, node2):
                return False
            
            graph.remove_edge(node1, node2)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_node_positions(graph: nx.Graph) -> Dict[str, Tuple[float, float]]:
        """노드 위치 정보 반환"""
        positions = {}
        for node, data in graph.nodes(data=True):
            if 'pos' in data:
                positions[node] = data['pos']
            else:
                # 기본 위치 설정 (spring layout 사용)
                pos = nx.spring_layout(graph)
                positions = pos
                break
        return positions
    
    @staticmethod
    def save_graph(graph: nx.Graph, filename: str) -> bool:
        """그래프를 JSON 파일로 저장"""
        try:
            # NetworkX 그래프를 JSON 형태로 변환
            data = {
                'nodes': [
                    {
                        'id': str(node),
                        'data': data
                    }
                    for node, data in graph.nodes(data=True)
                ],
                'edges': [
                    {
                        'source': str(edge[0]),
                        'target': str(edge[1])
                    }
                    for edge in graph.edges()
                ]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"그래프 저장 실패: {e}")
            return False
    
    @staticmethod
    def load_graph(filename: str) -> Optional[nx.Graph]:
        """JSON 파일에서 그래프 로드"""
        try:
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            G = nx.Graph()
            
            # 노드 추가
            for node_data in data['nodes']:
                G.add_node(node_data['id'], **node_data['data'])
            
            # 간선 추가
            for edge_data in data['edges']:
                G.add_edge(edge_data['source'], edge_data['target'])
            
            return G
        except Exception as e:
            print(f"그래프 로드 실패: {e}")
            return None
    
    @staticmethod
    def get_graph_stats(graph: nx.Graph) -> Dict[str, int]:
        """그래프 통계 정보 반환"""
        return {
            'nodes': graph.number_of_nodes(),
            'edges': graph.number_of_edges(),
            'components': nx.number_connected_components(graph),
            'max_degree': max(dict(graph.degree()).values()) if graph.nodes() else 0
        }
    
    @staticmethod
    def check_connectivity(graph: nx.Graph, start_node: str, target_node: str) -> Dict:
        """
        두 노드 간의 연결성 확인
        
        Args:
            graph: NetworkX 그래프
            start_node: 시작 노드
            target_node: 목표 노드
            
        Returns:
            연결성 정보 딕셔너리
        """
        try:
            if start_node not in graph or target_node not in graph:
                return {
                    'connected': False,
                    'path_exists': False,
                    'shortest_path': None,
                    'distance': float('inf'),
                    'error': '노드가 그래프에 존재하지 않습니다.'
                }
            
            # 연결성 확인
            is_connected = nx.is_connected(graph)
            
            # 경로 존재 여부 확인
            try:
                shortest_path = nx.shortest_path(graph, start_node, target_node)
                distance = len(shortest_path) - 1
                path_exists = True
            except nx.NetworkXNoPath:
                shortest_path = None
                distance = float('inf')
                path_exists = False
            
            return {
                'connected': is_connected,
                'path_exists': path_exists,
                'shortest_path': shortest_path,
                'distance': distance,
                'total_components': nx.number_connected_components(graph),
                'nodes_in_largest_component': len(max(nx.connected_components(graph), key=len)) if graph.nodes() else 0
            }
            
        except Exception as e:
            return {
                'connected': False,
                'path_exists': False,
                'shortest_path': None,
                'distance': float('inf'),
                'error': f'연결성 확인 중 오류: {e}'
            } 