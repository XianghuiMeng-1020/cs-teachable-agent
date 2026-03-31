def sort_space_stations(stations):
    sorted_stations = {f'{"Human" if key % 2 != 0 else "Teklar"} {key}': value for key, value in sorted(stations.items())}
    return sorted_stations