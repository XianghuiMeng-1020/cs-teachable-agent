def active_starships(log_lines):
    active_ships = []
    for line in log_lines:
        name, fuel = line.rsplit(' ', 1)
        if int(fuel) > 50:
            active_ships.append(name)
    return sorted(active_ships)