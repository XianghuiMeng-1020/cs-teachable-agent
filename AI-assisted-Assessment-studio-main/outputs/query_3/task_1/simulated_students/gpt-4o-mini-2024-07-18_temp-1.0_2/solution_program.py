def sort_space_stations(stations):
    sorted_stations = {}
    for station_number in sorted(stations.keys()):
        if station_number % 2 == 0:
            new_key = f'Teklar {station_number}'
        else:
            new_key = f'Human {station_number}'
        sorted_stations[new_key] = stations[station_number]
    return sorted_stations