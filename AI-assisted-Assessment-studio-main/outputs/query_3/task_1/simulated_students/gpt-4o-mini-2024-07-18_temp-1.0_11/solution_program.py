def sort_space_stations(stations):
    sorted_stations = {}
    for number in sorted(stations.keys()):
        prefix = "Human" if number % 2 != 0 else "Teklar"
        sorted_stations[f"{prefix} {number}"] = stations[number]
    return sorted_stations