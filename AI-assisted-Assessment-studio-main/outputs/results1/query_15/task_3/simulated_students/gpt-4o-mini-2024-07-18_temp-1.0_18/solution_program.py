def active_starships(log_lines):
    operational_ships = []
    for log in log_lines:
        name, fuel = log.rsplit(' ', 1)
        if int(fuel) > 50:
            operational_ships.append(name)
    return sorted(operational_ships)