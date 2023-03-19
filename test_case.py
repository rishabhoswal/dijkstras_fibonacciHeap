from dijkstras_algo import dijkstra_algo

# TestCase1: Test that the function returns the correct distance dictionary for a valid input graph and start node.
graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1)],
    'C': [('A', 3), ('B', 1), ('D', 4)],
    'D': [('C', 4)]
}
start_node = "B"
expected_distance = {'A': 2, 'B': 0, 'C': 1, 'D': 5}
assert dijkstra_algo(graph, start_node) == expected_distance

# TestCase2: Test that the function returns the correct distance dictionary for a graph with only one node.
graph = {'A': []}
start_node = "A"
expected_distance = {'A': 0}
assert dijkstra_algo(graph, start_node) == expected_distance

# Testcase 3: Test that the function returns the correct distance dictionary for a graph with disconnected nodes.
graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1)],
    'C': [('A', 3), ('B', 1)],
    'D': []
}
start_node = "A"
expected_distance = {'A': 0, 'B': 2, 'C': 3, 'D': float('inf')}
assert dijkstra_algo(graph, start_node) == expected_distance
