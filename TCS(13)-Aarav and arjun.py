import sys
import math
sys.setrecursionlimit(10000)

EPS = 1e-8

def nearly_equal(a,b,eps=EPS):
    return abs(a-b) <= eps

def orient(ax,ay,bx,by,cx,cy):
    # cross product (b-a) x (c-a)
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)

def on_segment(ax,ay,bx,by,px,py):
    # check p is on segment ab
    if abs(orient(ax,ay,bx,by,px,py)) > EPS:
        return False
    return min(ax,bx)-EPS <= px <= max(ax,bx)+EPS and min(ay,by)-EPS <= py <= max(ay,by)+EPS

def seg_intersection(a1,a2,b1,b2):
    # each param is (x,y)
    x1,y1 = a1; x2,y2 = a2; x3,y3 = b1; x4,y4 = b2
    # bounding boxes
    # compute orientations
    d1 = orient(x1,y1,x2,y2,x3,y3)
    d2 = orient(x1,y1,x2,y2,x4,y4)
    d3 = orient(x3,y3,x4,y4,x1,y1)
    d4 = orient(x3,y3,x4,y4,x2,y2)
    inters = []
    # General intersection (proper)
    if (d1*d2 < -EPS) and (d3*d4 < -EPS):
        # compute intersection point of two lines
        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if abs(denom) < EPS:
            return []
        ix = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
        iy = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom
        return [(ix,iy)]
    # collinear or touching endpoints cases
    # check endpoints of one on the other
    if abs(d1) <= EPS and on_segment(x1,y1,x2,y2,x3,y3):
        inters.append((x3,y3))
    if abs(d2) <= EPS and on_segment(x1,y1,x2,y2,x4,y4):
        inters.append((x4,y4))
    if abs(d3) <= EPS and on_segment(x3,y3,x4,y4,x1,y1):
        inters.append((x1,y1))
    if abs(d4) <= EPS and on_segment(x3,y3,x4,y4,x2,y2):
        inters.append((x2,y2))
    # Remove duplicates (close points)
    cleaned = []
    for p in inters:
        found = False
        for q in cleaned:
            if nearly_equal(p[0],q[0]) and nearly_equal(p[1],q[1]):
                found = True; break
        if not found:
            cleaned.append(p)
    return cleaned

def point_key(p):
    # round coordinates to stable representation keys
    return (round(p[0],8), round(p[1],8))

def dist(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    segs = []
    for _ in range(N):
        x1 = float(next(it)); y1 = float(next(it)); x2 = float(next(it)); y2 = float(next(it))
        segs.append(((x1,y1),(x2,y2)))
    # 1. collect all points: endpoints + intersections
    points_set = {}  # key -> (x,y)
    # helper to add point
    def add_point(p):
        k = point_key(p)
        if k not in points_set:
            points_set[k] = (p[0], p[1])
        return points_set[k]

    # add all endpoints
    for a,b in segs:
        add_point(a); add_point(b)
    # find intersections
    for i in range(N):
        for j in range(i+1,N):
            pts = seg_intersection(segs[i][0], segs[i][1], segs[j][0], segs[j][1])
            for p in pts:
                add_point(p)

    # 2. for each original segment, gather its split points, sort along the segment, and create atomic edges
    nodes = {}  # point_key -> index
    node_list = []
    for k,p in points_set.items():
        nodes[k] = len(node_list)
        node_list.append(p)

    adj = {}  # index -> dict{neighbor_index: length}
    for idx in range(len(node_list)):
        adj[idx] = {}

    for (a,b) in segs:
        # collect points lying on this segment
        pts = []
        ax,ay = a; bx,by = b
        seg_len = math.hypot(bx-ax, by-ay)
        if seg_len < EPS:
            continue
        for k,p in points_set.items():
            px,py = p
            if on_segment(ax,ay,bx,by,px,py):
                # compute param t along segment
                if abs(bx-ax) > abs(by-ay):
                    t = (px - ax) / (bx - ax) if abs(bx-ax) > EPS else 0.0
                else:
                    t = (py - ay) / (by - ay) if abs(by-ay) > EPS else 0.0
                pts.append((t, p))
        # sort by t
        pts.sort(key=lambda x: x[0])
        # create edges between consecutive distinct pts
        for i in range(len(pts)-1):
            p1 = pts[i][1]; p2 = pts[i+1][1]
            k1 = point_key(p1); k2 = point_key(p2)
            u = nodes[k1]; v = nodes[k2]
            if u == v:
                continue
            length = dist(p1,p2)
            # add undirected edge (avoid duplicates by min)
            if v not in adj[u] or adj[u][v] > length + 1e-9:
                adj[u][v] = length
                adj[v][u] = length

    # 3. Find any simple cycle in undirected graph with DFS
    n_nodes = len(node_list)
    visited = [False]*n_nodes
    parent = [-1]*n_nodes
    in_stack = [False]*n_nodes
    stack = []

    cycle = []  # will store node indices of cycle in order if found

    def dfs(u):
        nonlocal cycle
        visited[u] = True
        in_stack[u] = True
        stack.append(u)
        for v in adj[u].keys():
            if cycle:
                return
            if not visited[v]:
                parent[v] = u
                dfs(v)
                if cycle:
                    return
            elif in_stack[v] and v != parent[u]:
                # found cycle: collect nodes from stack top until v
                idx = len(stack)-1
                cyc = []
                while idx >= 0 and stack[idx] != v:
                    cyc.append(stack[idx])
                    idx -= 1
                cyc.append(v)
                cyc.reverse()
                # ensure at least 3 distinct nodes
                if len(cyc) >= 3:
                    cycle = cyc
                    return
        stack.pop()
        in_stack[u] = False

    for s in range(n_nodes):
        if not visited[s]:
            dfs(s)
        if cycle:
            break

    if not cycle:
        print("No")
        return

    # We have a cycle as sequence of node indices cycle[0..k-1]
    # Ensure edges exist between consecutive nodes and between last and first
    k = len(cycle)
    # compute polygon area (using coordinates in cycle order)
    poly = [node_list[i] for i in cycle]
    # closing edge
    # compute area
    area = 0.0
    for i in range(k):
        x1,y1 = poly[i]
        x2,y2 = poly[(i+1)%k]
        area += (x1*y2 - x2*y1)
    area = abs(area)/2.0

    # compute cycle perimeter by summing adj lengths between consecutive nodes
    perimeter = 0.0
    cycle_edges = set()
    for i in range(k):
        u = cycle[i]; v = cycle[(i+1)%k]
        # store edge key as ordered pair (min,max)
        key = (min(u,v), max(u,v))
        cycle_edges.add(key)
        if v not in adj[u]:
            # If adjacency missing, fallback to direct Euclidean distance
            perimeter += dist(node_list[u], node_list[v])
        else:
            perimeter += adj[u][v]

    # compute total length of all edges then leftover = total - perimeter_of_cycle_edges
    total_len = 0.0
    for u in range(n_nodes):
        for v,l in adj[u].items():
            if u < v:
                total_len += l
    # subtract cycle edges lengths once (they are part of total)
    cycle_len = 0.0
    for (u,v) in cycle_edges:
        cycle_len += adj[u][v]
    leftover = total_len - cycle_len

    # Check if Arjun can form same shape & size: leftover length >= perimeter (allow small epsilon)
    can_form = (leftover + 1e-6 >= perimeter)

    # Output
    print("Yes")
    print("Yes" if can_form else "No")
    print("{:.2f}".format(area))


if __name__ == "__main__":
    main()
