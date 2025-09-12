def clock_cost(initial_time, Q, A, B, X, Y, queries):
    # Parse time
    hour, minute = map(int, initial_time.split(":"))
    hour_angle = (hour % 12) * 30
    minute_angle = minute * 6

    total_cost = 0

    for target in queries:
        # Compute current angle
        diff = abs(hour_angle - minute_angle)
        curr_angles = {diff, 360 - diff}  # both possible

        if target in curr_angles:
            continue  # cost 0

        best = float("inf")

        # Try moving hands (hour CW / min CCW) and (hour CCW / min CW)
        for hour_dir, min_dir in [("CW", "CCW"), ("CCW", "CW")]:
            # Try moving the hour hand 0,1,...,11 steps (30° each)
            for steps in range(12):
                new_hour_angle = (hour_angle + steps * 30 if hour_dir=="CW" else hour_angle - steps * 30) % 360

                # Compute required minute angle
                for new_min_angle in range(0, 361):
                    diff = abs(new_hour_angle - new_min_angle)
                    if target in (diff, 360-diff):
                        # Compute costs
                        h_cost = abs(new_hour_angle - hour_angle) * X * (A if hour_dir=="CW" else B)
                        m_cost = abs(new_min_angle - minute_angle) * Y * (A if min_dir=="CW" else B)
                        best = min(best, h_cost + m_cost)

        total_cost += best

    return total_cost
