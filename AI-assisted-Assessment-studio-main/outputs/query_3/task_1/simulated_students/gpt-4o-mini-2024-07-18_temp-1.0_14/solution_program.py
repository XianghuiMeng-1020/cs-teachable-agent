def sort_space_stations(stations):
    sorted_stations = sorted(stations.items())
    result = {}
    for number, name in sorted_stations:
        prefix = "Human" if number % 2 != 0 else "Teklar"
        result[f"{prefix} {number}"] = name
    return result