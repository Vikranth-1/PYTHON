import heapq
from collections import defaultdict

def bus_count():
    M = int(input().strip())
    dist = [list(map(int, input().split())) for _ in range(M)]
    employees = list(map(int, input().split()))
    capacity = int(input().strip())

    # Insert 0 employees for office at index 0
    employees = [0] + employees

    # Step 1: Dijkstra to build shortest path tree
    pq = [(0, 0)]  # (distance, node)
    d = [float("inf")] * M
    parent = [-1] * M
    d[0] = 0

    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v in range(M):
            if u != v:
                nd = du + dist[u][v]
                if nd < d[v]:
                    d[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))

    # Step 2: Build tree adjacency from parent
    tree = defaultdict(list)
    for i in range(1, M):
        tree[parent[i]].append(i)

    buses_required = 0

    # Step 3: DFS post-order to compute buses
    def dfs(node):
        nonlocal buses_required
        total_emp = employees[node]

        for child in tree[node]:
            total_emp += dfs(child)

        full_buses = total_emp // capacity
        leftover = total_emp % capacity
        buses_required += full_buses
        return leftover  # carry leftover upward

    leftover = dfs(0)
    if leftover > 0:
        buses_required += 1

    print(buses_required)
