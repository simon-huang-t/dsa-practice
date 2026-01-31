'''
Longest Path in an Undirected Graph

The longest path problem in an undirected graph is about finding the longest simple path (no repeated vertices) 
between two vertices. This is NP-hard for general graphs, meaning there's no known efficient solution for large graphs. 
However, we can compute the longest path in a tree or connected acyclic graph 
using a well-known trick based on Breadth-First Search (BFS) or Depth-First Search (DFS).

Intuition
The idea is based on the diameter of the tree, which is the longest path between two nodes. 
For any tree, this longest path is found as follows:
1) Start with any node (say node A) and run BFS/DFS to find the farthest node from A (say node B).
2) Run BFS/DFS again starting from node B to find the farthest node from B (say node C).
3) The longest path will be the path between nodes B and C.
This works because the longest path in a tree always lies between two leaf nodes, and BFS/DFS helps you find this path efficiently.

Steps for the Longest Path in an Undirected Graph
1) Pick any node in the graph.
2) Run BFS/DFS from that node to find the farthest node, let’s call it farthest_node_1.
3) Run BFS/DFS starting from farthest_node_1 to find the farthest node from it, called farthest_node_2.
4) The distance between farthest_node_1 and farthest_node_2 is the longest path in the graph.

This algorithm works because:
Any longest path in a tree will lie between two leaf nodes.
The farthest node found from any arbitrary node in the graph is guaranteed to be one end of the longest path.


Time Complexity
BFS runs in O(V + E) where V is the number of vertices and E is the number of edges.
We run BFS twice, so the total time complexity is O(V + E).

Space Complexity
The space complexity is O(V) due to the distance array and the queue used for BFS.

Handling Disconnected Graphs
If the graph is disconnected, you'll need to handle each connected component separately. You can either:
1) Perform BFS/DFS starting from each unvisited node.
2) If a disconnected component has no edges, the longest path is just 0.
'''
from collections import deque

# BFS to find the farthest node and its distance
def bfs(graph, start):
    n = len(graph)
    distance = [-1] * n  # -1 means unvisited
    distance[start] = 0
    q = deque([start])

    farthest_node = start
    max_distance = 0

    while q:
        node = q.popleft()

        for neighbor in graph[node]:
            if distance[neighbor] == -1:  # If neighbor hasn't been visited
                distance[neighbor] = distance[node] + 1
                q.append(neighbor)

                if distance[neighbor] > max_distance:
                    max_distance = distance[neighbor]
                    farthest_node = neighbor

    return farthest_node, max_distance

def longest_path_in_graph(graph):
    # Start BFS from any node (usually node 0 if the graph is connected)
    start_node = 0
    farthest_node_1, _ = bfs(graph, start_node)

    # Run BFS again from the farthest node found
    farthest_node_2, longest_path_length = bfs(graph, farthest_node_1)

    return longest_path_length, farthest_node_1, farthest_node_2

# Example graph (adjacency list)
graph = [
    [1, 2],    # Node 0 is connected to nodes 1 and 2
    [0, 3],    # Node 1 is connected to nodes 0 and 3
    [0, 3],    # Node 2 is connected to nodes 0 and 3
    [1, 2, 4], # Node 3 is connected to nodes 1, 2, and 4
    [3]        # Node 4 is connected to node 3
]

longest_path_length, node_1, node_2 = longest_path_in_graph(graph)
print(f"Longest path length: {longest_path_length}")
print(f"Longest path between node {node_1} and node {node_2}")

# Test cases
def test_longest_path():
    # Test Case 1: Simple graph (tree-like structure)
    graph1 = [
        [1, 2],    # Node 0 is connected to nodes 1 and 2
        [0, 3],    # Node 1 is connected to nodes 0 and 3
        [0, 3],    # Node 2 is connected to nodes 0 and 3
        [1, 2, 4], # Node 3 is connected to nodes 1, 2, and 4
        [3]        # Node 4 is connected to node 3
    ]
    longest_path_length, node_1, node_2 = longest_path_in_graph(graph1)
    assert longest_path_length == 4, f"Test case 1 failed: expected 4, got {longest_path_length}"
    assert (node_1 == 1 and node_2 == 4) or (node_1 == 4 and node_2 == 1), "Test case 1 failed: expected path between nodes 1 and 4"
    
    # Test Case 2: A simple linear graph
    graph2 = [
        [1],    # Node 0 is connected to node 1
        [0, 2], # Node 1 is connected to nodes 0 and 2
        [1, 3], # Node 2 is connected to nodes 1 and 3
        [2]     # Node 3 is connected to node 2
    ]
    longest_path_length, node_1, node_2 = longest_path_in_graph(graph2)
    assert longest_path_length == 3, f"Test case 2 failed: expected 3, got {longest_path_length}"
    assert (node_1 == 0 and node_2 == 3) or (node_1 == 3 and node_2 == 0), "Test case 2 failed: expected path between nodes 0 and 3"
    
    # Test Case 3: Disconnected graph
    graph3 = [
        [1],   # Node 0 is connected to node 1
        [0],   # Node 1 is connected to node 0
        [3],   # Node 2 is connected to node 3
        [2]    # Node 3 is connected to node 2
    ]
    longest_path_length, node_1, node_2 = longest_path_in_graph(graph3)
    assert longest_path_length == 2, f"Test case 3 failed: expected 2, got {longest_path_length}"
    assert (node_1 == 2 and node_2 == 3) or (node_1 == 3 and node_2 == 2), "Test case 3 failed: expected path between nodes 2 and 3"
    
    # Test Case 4: A graph with no edges (trivial case)
    graph4 = [
        [],  # Node 0 has no neighbors
        []   # Node 1 has no neighbors
    ]
    longest_path_length, node_1, node_2 = longest_path_in_graph(graph4)
    assert longest_path_length == 0, f"Test case 4 failed: expected 0, got {longest_path_length}"
    assert node_1 == node_2 == 0, "Test case 4 failed: expected path between node 0 and node 0"

    print("All test cases passed!")

# Run tests
test_longest_path()