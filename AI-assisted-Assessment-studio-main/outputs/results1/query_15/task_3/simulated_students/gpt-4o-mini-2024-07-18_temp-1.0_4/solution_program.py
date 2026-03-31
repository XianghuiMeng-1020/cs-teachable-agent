def active_starships(log_lines):
    operational_starships = []
    for entry in log_lines:
        name, fuel = entry.split()
        if int(fuel) > 50:
            operational_starships.append(name)
    return sorted(operational_starships)