def active_starships(log_lines):
    operational = []
    for line in log_lines:
        name, fuel = line.rsplit(' ', 1)
        if int(fuel) > 50:
            operational.append(name)
    return sorted(operational)