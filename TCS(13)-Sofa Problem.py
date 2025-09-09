from collections import deque

def sofa_problem(M, N, grid):
    # Find start & goal positions
    start, goal = [], []
    for r in range(M):
        for c in range(N):
            if grid[r][c] == "s":
                start.append((r, c))
            if grid[r][c] == "S":
                goal.append((r, c))

    # Determine orientation
    def orientation(cells):
        (r1, c1), (r2, c2) = cells
        return "H" if r1 == r2 else "V"

    start_state = (min(start), orientation(start))
    goal_state  = (min(goal), orientation(goal))

    # BFS setup
    q = deque([(start_state, 0)])  # (state, steps)
    visited = set([start_state])

    while q:
        (pos, ori), steps = q.popleft()

        # Check goal
        if (pos, ori) == goal_state:
            return steps

        r, c = pos

        # Possible moves
        moves = []

        if ori == "H":
            # Horizontal sofa occupies (r,c) & (r,c+1)
            if c > 0 and grid[r][c-1] == "0":  # left
                moves.append(((r, c-1), "H"))
            if c+2 < N and grid[r][c+2] == "0":  # right
                moves.append(((r, c+1), "H"))
            if r > 0 and grid[r-1][c] == grid[r-1][c+1] == "0":  # up
                moves.append(((r-1, c), "H"))
            if r+1 < M and grid[r+1][c] == grid[r+1][c+1] == "0":  # down
                moves.append(((r+1, c), "H"))
            # Rotation check (inside 2x2)
            if r+1 < M and c+1 < N and grid[r][c] != "H" and grid[r][c+1] != "H" and grid[r+1][c] != "H" and grid[r+1][c+1] != "H":
                moves.append(((r, c), "V"))
                moves.append(((r, c+1), "V"))

        if ori == "V":
            # Vertical sofa occupies (r,c) & (r+1,c)
            if r > 0 and grid[r-1][c] == "0":
                moves.append(((r-1, c), "V"))
            if r+2 < M and grid[r+2][c] == "0":
                moves.append(((r+1, c), "V"))
            if c > 0 and grid[r][c-1] == grid[r+1][c-1] == "0":
                moves.append(((r, c-1), "V"))
            if c+1 < N and grid[r][c+1] == grid[r+1][c+1] == "0":
                moves.append(((r, c+1), "V"))
            # Rotation check
            if r+1 < M and c+1 < N and grid[r][c] != "H" and grid[r+1][c] != "H" and grid[r][c+1] != "H" and grid[r+1][c+1] != "H":
                moves.append(((r, c), "H"))
                moves.append(((r+1, c), "H"))

        # Add valid moves
        for new_state in moves:
            if new_state not in visited:
                visited.add(new_state)
                q.append((new_state, steps+1))

    return "Impossible"
