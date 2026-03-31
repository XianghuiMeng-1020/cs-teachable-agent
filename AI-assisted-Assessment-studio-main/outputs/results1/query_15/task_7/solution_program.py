def check_maintenance(distances):
    results = []
    for distance in distances:
        if distance % 1000 == 0:
            results.append("Check required")
        else:
            results.append("No check needed")
    return results