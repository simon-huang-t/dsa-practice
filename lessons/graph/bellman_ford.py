def bellman_ford(n, edges, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    # Relax all edges n-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    # Optional: detect negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # negative cycle exists

    return dist
