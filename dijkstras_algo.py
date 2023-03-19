from math import inf
from typing import Dict, List, Tuple

from fibonacci_heap import FibonacciHeap


def dijkstra_algo(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Dict[str, int]:
    distance = {node: inf for node in graph}
    distance[start_node] = 0

    heap = FibonacciHeap()
    heap.add_node(0, start_node)

    visited = set()

    while not heap.is_empty():
        _, node = heap.remove_min_node()
        visited.add(node)

        for adjacent_node, weight in graph[node.value]:
            if adjacent_node not in visited:
                new_distance = distance[node.value] + weight
                if new_distance < distance[adjacent_node]:
                    distance[adjacent_node] = new_distance
                    if heap.find_node(adjacent_node):
                        heap.decrease_key(heap.find_node(adjacent_node), new_distance)
                    else:
                        heap.add_node(new_distance, adjacent_node)
    return distance
