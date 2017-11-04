import collections


def _residual_capacity(G, u, v):
    return G[u][v]['capacity'] - G[u][v]['flow']


def _bfs(G, s, t, path):
    visited = {node: False for node in G}
    queue = collections.deque()
    queue.append(s)
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in G[u]:
            if _residual_capacity(G, u, v) > 0 and visited[v] is False:
                queue.append(v)
                visited[v] = True
                path[v] = u
    return visited[t]


def edmonds_karp(G, s, t):
    g = G.copy()
    for u, v in G.edges:
        g[u][v]['flow'] = 0
        if not G.has_edge(v, u):
            g.add_edge(v, u, capacity=0, flow=0)

    max_flow = 0
    path = {node: None for node in g}

    while _bfs(g, s, t, path):
        path_flow = float('inf')
        v = t
        while v != s:
            path_flow = min(path_flow, _residual_capacity(g, path[v], v))
            v = path[v]
        max_flow += path_flow
        v = t
        while v != s:
            u = path[v]
            g[u][v]['flow'] += path_flow
            g[v][u]['flow'] = -g[u][v]['flow']
            v = u
    g.graph['max_flow'] = max_flow
    return g
