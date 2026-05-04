'''
Dijkstra's algorithm is a graph search algorithm that finds 
the shortest path between nodes in a graph. 
It is a greedy algorithm and works on weighted graphs.
'''

def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

# --- TEST CASE ---

# Graph Structure:
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

start_node = 0
distances = dijkstra(graph, start_node)

print(f"Shortest distances from node {start_node}: {distances}")
