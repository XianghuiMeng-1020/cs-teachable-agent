def sort_space_stations(stations):
    sorted_stations = {}
    for key in sorted(stations.keys()):
        prefix = 'Teklar' if key % 2 == 0 else 'Human'
        new_key = f"{prefix} {key}"
        sorted_stations[new_key] = stations[key]
    return sorted_stations