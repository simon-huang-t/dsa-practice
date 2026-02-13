from collections import defaultdict, deque
from typing import List

def kahn_toposort(n: int, edges: List[List[int]]) -> List[int]:
    """
    n: number of nodes (0 to n-1)
    edges: list of [u, v] meaning u -> v
    Returns topological order if DAG, else empty list
    """
    # Build graph and in-degree
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Queue of nodes with 0 in-degree
    q = deque([i for i in range(n) if in_degree[i] == 0])
    topo = []

    while q:
        node = q.popleft()
        topo.append(node)
        for nei in graph[node]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                q.append(nei)

    # If topo contains all nodes, return it; else cycle exists
    if len(topo) == n:
        return topo
    else:
        return []  # graph has a cycle
