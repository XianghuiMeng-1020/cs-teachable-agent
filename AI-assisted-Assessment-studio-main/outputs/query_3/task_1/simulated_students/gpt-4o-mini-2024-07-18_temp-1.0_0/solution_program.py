def sort_space_stations(stations):
    sorted_stations = {}  
    for number in sorted(stations.keys()):
        if number % 2 == 0:
            new_key = f'Teklar {number}'
        else:
            new_key = f'Human {number}'
        sorted_stations[new_key] = stations[number]
    return sorted_stations