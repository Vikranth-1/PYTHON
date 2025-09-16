def bands_problem():
    S = int(input().strip())
    grid = [list(input().strip()) for _ in range(S)]

    # Directions: up, down, left, right
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    def collect_band(ch):
        cells = []
        for r in range(S):
            for c in range(S):
                if grid[r][c] == ch:
                    cells.append((r,c))
        return set(cells)

    band1 = collect_band("1")
    band2 = collect_band("2")

    # Find overlaps: cells where paths cross
    overlaps = set()
    for r,c in band1:
        for dr,dc in dirs:
            nr,nc = r+dr, c+dc
            if (nr,nc) in band2:
                # If band1 and band2 cross at right angle
                overlaps.add((r,c))

    # Function to test connectivity ignoring overlaps
    def is_connected(cells, overlaps):
        if not cells:
            return True
        start = next(iter(cells))
        stack = [start]
        visited = set([start])
        while stack:
            r,c = stack.pop()
            for dr,dc in dirs:
                nr,nc = r+dr,c+dc
                if (nr,nc) in cells and (nr,nc) not in visited and (nr,nc) not in overlaps:
                    visited.add((nr,nc))
                    stack.append((nr,nc))
        # All cells except overlap must be visited
        return all(cell in visited or cell in overlaps for cell in cells)

    if not is_connected(band1, overlaps) or not is_connected(band2, overlaps):
        print("Impossible")
    else:
        print(len(overlaps))
