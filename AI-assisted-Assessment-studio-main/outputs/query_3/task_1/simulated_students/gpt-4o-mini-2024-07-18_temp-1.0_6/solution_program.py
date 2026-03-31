def sort_space_stations(stations):
    sorted_stations = {}
    for station_number in sorted(stations.keys()):
        prefix = "Human" if station_number % 2 != 0 else "Teklar"
        new_key = f"{prefix} {station_number}"
        sorted_stations[new_key] = stations[station_number]
    return sorted_stations