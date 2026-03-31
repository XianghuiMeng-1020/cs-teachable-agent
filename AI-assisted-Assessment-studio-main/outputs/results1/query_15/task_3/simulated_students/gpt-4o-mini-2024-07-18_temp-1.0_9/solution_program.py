def active_starships(log_lines):
    operational_starships = []
    for log in log_lines:
        name, fuel = log.rsplit(' ', 1)
        if int(fuel) > 50:
            operational_starships.append(name)
    return sorted(operational_starships)