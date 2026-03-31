def sort_space_stations(stations):
    sorted_stations = dict()
    for num in sorted(stations.keys()):
        prefix = "Human" if num % 2 != 0 else "Teklar"
        new_key = f"{prefix} {num}"
        sorted_stations[new_key] = stations[num]
    return sorted_stations