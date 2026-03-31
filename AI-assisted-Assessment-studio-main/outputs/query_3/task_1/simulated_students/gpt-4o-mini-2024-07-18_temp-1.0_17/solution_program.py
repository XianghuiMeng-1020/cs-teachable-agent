def sort_space_stations(stations):
    sorted_stations = {}
    for key in sorted(stations.keys()):
        if key % 2 == 0:
            new_key = f'Teklar {key}'
        else:
            new_key = f'Human {key}'
        sorted_stations[new_key] = stations[key]
    return sorted_stations