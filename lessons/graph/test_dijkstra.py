'''
Tests for Dijkstra's shortest-path algorithm.

Graph representation: dict mapping each node (0-indexed int) to a list of
(neighbor, weight) tuples.  All edge weights must be non-negative.
'''
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dijkstra import dijkstra


def test_pr_example_graph():
    # Exact graph from the PR diff
    # 0 --(4)--> 1
    # 0 --(1)--> 2
    # 2 --(2)--> 1
    # 1 --(5)--> 3
    # 2 --(8)--> 3
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 5)],
        2: [(1, 2), (3, 8)],
        3: []
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0,           f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 3,           f"Expected dist[1]=3 (0->2->1), got {dist[1]}"
    assert dist[2] == 1,           f"Expected dist[2]=1 (0->2), got {dist[2]}"
    assert dist[3] == 8,           f"Expected dist[3]=8 (0->2->1->3), got {dist[3]}"


def test_start_from_different_node():
    # Same graph topology, starting from node 2
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 5)],
        2: [(1, 2), (3, 8)],
        3: []
    }
    dist = dijkstra(graph, 2)
    # From node 2: 2->1 (weight 2), 2->3 (weight 8), 2->1->3 (weight 7)
    assert dist[0] == float('inf'), f"Expected dist[0]=inf (no path to 0), got {dist[0]}"
    assert dist[1] == 2,            f"Expected dist[1]=2 (2->1), got {dist[1]}"
    assert dist[2] == 0,            f"Expected dist[2]=0 (start), got {dist[2]}"
    assert dist[3] == 7,            f"Expected dist[3]=7 (2->1->3), got {dist[3]}"


def test_single_node_graph():
    # Only one node, no edges
    graph = {0: []}
    dist = dijkstra(graph, 0)
    assert dist == [0], f"Expected [0], got {dist}"


def test_two_nodes_direct_edge():
    # 0 --(7)--> 1
    graph = {
        0: [(1, 7)],
        1: []
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 7, f"Expected dist[1]=7, got {dist[1]}"


def test_linear_chain():
    # 0 --(1)--> 1 --(2)--> 2 --(3)--> 3
    graph = {
        0: [(1, 1)],
        1: [(2, 2)],
        2: [(3, 3)],
        3: []
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 1, f"Expected dist[1]=1, got {dist[1]}"
    assert dist[2] == 3, f"Expected dist[2]=3, got {dist[2]}"
    assert dist[3] == 6, f"Expected dist[3]=6, got {dist[3]}"


def test_direct_path_cheaper_than_indirect():
    # 0 --(2)--> 1 (direct cheaper than going through 2)
    # 0 --(1)--> 2 --(5)--> 1
    graph = {
        0: [(1, 2), (2, 1)],
        1: [],
        2: [(1, 5)]
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 2, f"Expected dist[1]=2 (direct), got {dist[1]}"
    assert dist[2] == 1, f"Expected dist[2]=1, got {dist[2]}"


def test_indirect_path_cheaper_than_direct():
    # PR pattern: 0 --(10)--> 1, but 0 --(1)--> 2 --(2)--> 1 is cheaper
    graph = {
        0: [(1, 10), (2, 1)],
        1: [],
        2: [(1, 2)]
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 3, f"Expected dist[1]=3 (0->2->1), got {dist[1]}"
    assert dist[2] == 1, f"Expected dist[2]=1, got {dist[2]}"


def test_unreachable_node():
    # Node 2 has no incoming edges from the connected component of 0
    # Directed: 0->1, 2->0 (2 can reach 0 but 0 cannot reach 2)
    graph = {
        0: [(1, 3)],
        1: [],
        2: [(0, 1)]
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0,            f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 3,            f"Expected dist[1]=3, got {dist[1]}"
    assert dist[2] == float('inf'), f"Expected dist[2]=inf, got {dist[2]}"


def test_start_node_with_no_outgoing_edges():
    # Starting from a node that has no outgoing edges; all other nodes unreachable
    graph = {
        0: [],
        1: [(0, 2)],
        2: [(1, 4)]
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0,            f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == float('inf'), f"Expected dist[1]=inf, got {dist[1]}"
    assert dist[2] == float('inf'), f"Expected dist[2]=inf, got {dist[2]}"


def test_equal_cost_paths():
    # Two paths of identical total cost to node 2
    # 0 --(3)--> 2  and  0 --(1)--> 1 --(2)--> 2  (both cost 3)
    graph = {
        0: [(1, 1), (2, 3)],
        1: [(2, 2)],
        2: []
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 1, f"Expected dist[1]=1, got {dist[1]}"
    assert dist[2] == 3, f"Expected dist[2]=3, got {dist[2]}"


def test_multiple_paths_complex_graph():
    # More complex graph with 5 nodes
    # Verify that the algorithm always finds the globally optimal path
    graph = {
        0: [(1, 10), (2, 3)],
        1: [(3, 2)],
        2: [(1, 4), (3, 8), (4, 2)],
        3: [(4, 5)],
        4: [(3, 1)]
    }
    dist = dijkstra(graph, 0)
    # 0->2 = 3
    # 0->2->1 = 3+4 = 7  (better than direct 10)
    # 0->2->1->3 = 7+2 = 9  (better than 0->2->3=11)
    # 0->2->4 = 3+2 = 5
    # 0->2->4->3 = 5+1 = 6  (better than 9)
    assert dist[0] == 0,  f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 7,  f"Expected dist[1]=7, got {dist[1]}"
    assert dist[2] == 3,  f"Expected dist[2]=3, got {dist[2]}"
    assert dist[3] == 6,  f"Expected dist[3]=6, got {dist[3]}"
    assert dist[4] == 5,  f"Expected dist[4]=5, got {dist[4]}"


def test_zero_weight_edges():
    # Zero-weight edges should be handled correctly (still non-negative)
    graph = {
        0: [(1, 0), (2, 5)],
        1: [(2, 5)],
        2: []
    }
    dist = dijkstra(graph, 0)
    assert dist[0] == 0, f"Expected dist[0]=0, got {dist[0]}"
    assert dist[1] == 0, f"Expected dist[1]=0, got {dist[1]}"
    assert dist[2] == 5, f"Expected dist[2]=5, got {dist[2]}"


def test_start_node_distance_is_always_zero():
    # Regression: the start node must always have distance 0 regardless of graph size
    graph = {
        0: [(1, 99), (2, 99), (3, 99)],
        1: [],
        2: [],
        3: []
    }
    for start in range(4):
        dist = dijkstra(graph, start)
        assert dist[start] == 0, f"Expected dist[{start}]=0 when starting from {start}, got {dist[start]}"


# Run all tests
test_pr_example_graph()
test_start_from_different_node()
test_single_node_graph()
test_two_nodes_direct_edge()
test_linear_chain()
test_direct_path_cheaper_than_indirect()
test_indirect_path_cheaper_than_direct()
test_unreachable_node()
test_start_node_with_no_outgoing_edges()
test_equal_cost_paths()
test_multiple_paths_complex_graph()
test_zero_weight_edges()
test_start_node_distance_is_always_zero()

print("All test cases passed!")
