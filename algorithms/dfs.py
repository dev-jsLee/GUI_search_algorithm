"""
DFS (깊이 우선 탐색) 알고리즘 구현
"""

import networkx as nx
from typing import List, Set, Dict, Optional, Generator, Tuple


class DFS:
    """깊이 우선 탐색 알고리즘 클래스"""
    
    def __init__(self, graph: nx.Graph):
        """
        DFS 초기화
        
        Args:
            graph: NetworkX 그래프
        """
        self.graph = graph
        self.reset()
    
    def reset(self):
        """알고리즘 상태 초기화"""
        self.visited: Set[str] = set()
        self.visit_order: List[str] = []
        self.current_path: List[str] = []
        self.stack: List[str] = []
        self.steps: List[Dict] = []
        self.current_step = 0
        self.is_complete = False
    
    def search(self, start_node: str, target_node: Optional[str] = None) -> Generator[Dict, None, None]:
        """
        DFS 탐색 실행 (제너레이터로 단계별 실행)
        
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
        
        # 스택에 시작 노드 추가
        self.stack.append(start_node)
        
        step_count = 0
        while self.stack:
            step_count += 1
            
            # 현재 노드를 스택에서 꺼냄
            current_node = self.stack.pop()
            
            # 이미 방문한 노드는 건너뛰기
            if current_node in self.visited:
                continue
            
            # 노드 방문 처리
            self.visited.add(current_node)
            self.visit_order.append(current_node)
            self.current_path.append(current_node)
            
            # 현재 단계 정보 저장
            step_info = {
                'step': step_count,
                'action': 'visit',
                'current_node': current_node,
                'visited': self.visited.copy(),
                'visit_order': self.visit_order.copy(),
                'stack': self.stack.copy(),
                'current_path': self.current_path.copy(),
                'message': f"노드 '{current_node}' 방문",
                'found_target': False
            }
            
            # 목표 노드를 찾은 경우
            if target_node and current_node == target_node:
                step_info['found_target'] = True
                step_info['message'] = f"목표 노드 '{target_node}' 발견!"
                self.steps.append(step_info)
                yield step_info
                self.is_complete = True
                return
            
            self.steps.append(step_info)
            yield step_info
            
            # 인접한 노드들을 스택에 추가 (역순으로 추가하여 알파벳 순서로 방문)
            neighbors = list(self.graph.neighbors(current_node))
            neighbors.sort(reverse=True)  # 역순 정렬
            
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.stack.append(neighbor)
            
            # 스택 상태 업데이트
            if self.stack:
                step_count += 1
                stack_info = {
                    'step': step_count,
                    'action': 'stack_update',
                    'current_node': current_node,
                    'visited': self.visited.copy(),
                    'visit_order': self.visit_order.copy(),
                    'stack': self.stack.copy(),
                    'current_path': self.current_path.copy(),
                    'message': f"스택에 인접 노드들 추가: {neighbors[::-1]}",
                    'found_target': False
                }
                self.steps.append(stack_info)
                yield stack_info
        
        # 탐색 완료
        final_step = {
            'step': step_count + 1,
            'action': 'complete',
            'current_node': None,
            'visited': self.visited.copy(),
            'visit_order': self.visit_order.copy(),
            'stack': [],
            'current_path': self.current_path.copy(),
            'message': '탐색 완료!',
            'found_target': target_node in self.visited if target_node else True
        }
        
        self.steps.append(final_step)
        self.is_complete = True
        yield final_step
    
    def get_path_to_node(self, target_node: str) -> Optional[List[str]]:
        """
        특정 노드까지의 경로 반환 (실제로는 DFS에서 정확한 경로를 구하기 어려움)
        
        Args:
            target_node: 목표 노드
            
        Returns:
            경로 리스트 또는 None
        """
        if target_node not in self.visited:
            return None
        
        # DFS에서는 방문 순서가 곧 경로가 아니므로,
        # 간단히 방문 순서에서 목표 노드까지만 반환
        try:
            target_index = self.visit_order.index(target_node)
            return self.visit_order[:target_index + 1]
        except ValueError:
            return None
    
    def get_statistics(self) -> Dict:
        """탐색 통계 정보 반환"""
        total_nodes = len(self.graph.nodes())
        visited_count = len(self.visited)
        
        return {
            'total_nodes': total_nodes,
            'visited_nodes': visited_count,
            'unvisited_nodes': total_nodes - visited_count,
            'visit_order': self.visit_order.copy(),
            'total_steps': len(self.steps),
            'algorithm': 'DFS',
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