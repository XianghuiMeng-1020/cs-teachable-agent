def check_maintenance(distances):
    return ["Check required" if distance % 1000 == 0 else "No check needed" for distance in distances]