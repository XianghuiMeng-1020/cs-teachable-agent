def sort_space_stations(stations):
    sorted_stations = sorted(stations.items())
    result = {}
    for number, name in sorted_stations:
        if number % 2 == 0:
            result[f'Teklar {number}'] = name
        else:
            result[f'Human {number}'] = name
    return result