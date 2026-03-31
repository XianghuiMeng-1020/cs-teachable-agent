def sort_space_stations(stations):
    sorted_stations = {}
    for key in sorted(stations.keys()):
        prefix = "Human" if key % 2 != 0 else "Teklar"
        new_key = f"{prefix} {key}"
        sorted_stations[new_key] = stations[key]
    return sorted_stations