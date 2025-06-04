"""
BFS (너비 우선 탐색) 알고리즘 구현
"""

import networkx as nx
from collections import deque
from typing import List, Set, Dict, Optional, Generator, Tuple


class BFS:
    """너비 우선 탐색 알고리즘 클래스"""
    
    def __init__(self, graph: nx.Graph):
        """
        BFS 초기화
        
        Args:
            graph: NetworkX 그래프
        """
        self.graph = graph
        self.reset()
    
    def reset(self):
        """알고리즘 상태 초기화"""
        self.visited: Set[str] = set()
        self.visit_order: List[str] = []
        self.queue: deque = deque()
        self.parent: Dict[str, Optional[str]] = {}
        self.level: Dict[str, int] = {}
        self.steps: List[Dict] = []
        self.current_step = 0
        self.is_complete = False
    
    def search(self, start_node: str, target_node: Optional[str] = None) -> Generator[Dict, None, None]:
        """
        BFS 탐색 실행 (제너레이터로 단계별 실행)
        
        Args:
            start_node: 시작 노드
            target_node: 목표 노드 (None이면 전체 탐색)
            
        Yields:
            각 단계의 상태 정보
        """
        self.reset()
        
        if start_node not in self.graph:
            yield {
                'error': f"시작 노드 '{start_node}'가 그래프에 존재하지 않습니다."
            }
            return
        
        # 큐에 시작 노드 추가
        self.queue.append(start_node)
        self.visited.add(start_node)
        self.parent[start_node] = None
        self.level[start_node] = 0
        
        step_count = 0
        
        while self.queue:
            step_count += 1
            
            # 큐에서 노드 꺼내기
            current_node = self.queue.popleft()
            self.visit_order.append(current_node)
            
            # 현재 단계 정보 저장
            step_info = {
                'step': step_count,
                'action': 'visit',
                'current_node': current_node,
                'visited': self.visited.copy(),
                'visit_order': self.visit_order.copy(),
                'queue': list(self.queue),
                'level': self.level.copy(),
                'message': f"노드 '{current_node}' 방문 (레벨: {self.level[current_node]})",
                'found_target': False
            }
            
            # 목표 노드를 찾은 경우
            if target_node and current_node == target_node:
                step_info['found_target'] = True
                step_info['message'] = f"목표 노드 '{target_node}' 발견! (레벨: {self.level[current_node]})"
                self.steps.append(step_info)
                yield step_info
                self.is_complete = True
                return
            
            self.steps.append(step_info)
            yield step_info
            
            # 인접한 노드들을 큐에 추가
            neighbors = list(self.graph.neighbors(current_node))
            neighbors.sort()  # 알파벳 순서로 정렬
            
            added_neighbors = []
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent[neighbor] = current_node
                    self.level[neighbor] = self.level[current_node] + 1
                    self.queue.append(neighbor)
                    added_neighbors.append(neighbor)
            
            # 큐 업데이트 단계
            if added_neighbors:
                step_count += 1
                queue_info = {
                    'step': step_count,
                    'action': 'queue_update',
                    'current_node': current_node,
                    'visited': self.visited.copy(),
                    'visit_order': self.visit_order.copy(),
                    'queue': list(self.queue),
                    'level': self.level.copy(),
                    'message': f"큐에 인접 노드들 추가: {added_neighbors}",
                    'found_target': False,
                    'added_neighbors': added_neighbors
                }
                self.steps.append(queue_info)
                yield queue_info
        
        # 탐색 완료
        final_step = {
            'step': step_count + 1,
            'action': 'complete',
            'current_node': None,
            'visited': self.visited.copy(),
            'visit_order': self.visit_order.copy(),
            'queue': [],
            'level': self.level.copy(),
            'message': '탐색 완료!',
            'found_target': target_node in self.visited if target_node else True
        }
        
        self.steps.append(final_step)
        self.is_complete = True
        yield final_step
    
    def get_path_to_node(self, target_node: str) -> Optional[List[str]]:
        """
        특정 노드까지의 최단 경로 반환
        
        Args:
            target_node: 목표 노드
            
        Returns:
            최단 경로 리스트 또는 None
        """
        if target_node not in self.visited or target_node not in self.parent:
            return None
        
        path = []
        current = target_node
        
        while current is not None:
            path.append(current)
            current = self.parent[current]
        
        return path[::-1]  # 역순으로 반환하여 시작->목표 순서로 만듦
    
    def get_shortest_distance(self, target_node: str) -> Optional[int]:
        """
        특정 노드까지의 최단 거리 반환
        
        Args:
            target_node: 목표 노드
            
        Returns:
            최단 거리 또는 None
        """
        if target_node in self.level:
            return self.level[target_node]
        return None
    
    def get_nodes_at_level(self, level: int) -> List[str]:
        """
        특정 레벨의 모든 노드들 반환
        
        Args:
            level: 레벨 번호
            
        Returns:
            해당 레벨의 노드 리스트
        """
        return [node for node, node_level in self.level.items() if node_level == level]
    
    def get_statistics(self) -> Dict:
        """탐색 통계 정보 반환"""
        total_nodes = len(self.graph.nodes())
        visited_count = len(self.visited)
        max_level = max(self.level.values()) if self.level else 0
        
        # 레벨별 노드 수 계산
        level_counts = {}
        for level in range(max_level + 1):
            level_counts[level] = len(self.get_nodes_at_level(level))
        
        return {
            'total_nodes': total_nodes,
            'visited_nodes': visited_count,
            'unvisited_nodes': total_nodes - visited_count,
            'visit_order': self.visit_order.copy(),
            'total_steps': len(self.steps),
            'algorithm': 'BFS',
            'max_level': max_level,
            'level_counts': level_counts,
            'completion_rate': (visited_count / total_nodes * 100) if total_nodes > 0 else 0
        }
    
    def get_step(self, step_number: int) -> Optional[Dict]:
        """특정 단계의 정보 반환"""
        if 0 <= step_number < len(self.steps):
            return self.steps[step_number]
        return None
    
    def get_all_steps(self) -> List[Dict]:
        """모든 단계의 정보 반환"""
        return self.steps.copy()
    
    def is_node_visited(self, node: str) -> bool:
        """노드가 방문되었는지 확인"""
        return node in self.visited
    
    def get_visit_time(self, node: str) -> Optional[int]:
        """노드가 몇 번째로 방문되었는지 반환"""
        try:
            return self.visit_order.index(node) + 1
        except ValueError:
            return None
    
    def get_node_level(self, node: str) -> Optional[int]:
        """노드의 레벨 반환"""
        return self.level.get(node)
    
    def get_parent(self, node: str) -> Optional[str]:
        """노드의 부모 노드 반환"""
        return self.parent.get(node)
    
    def get_tree_edges(self) -> List[Tuple[str, str]]:
        """BFS 트리의 간선들 반환"""
        tree_edges = []
        for node, parent in self.parent.items():
            if parent is not None:
                tree_edges.append((parent, node))
        return tree_edges 