def sort_space_stations(stations):
    sorted_stations = sorted(stations.items())
    result = {}
    for number, name in sorted_stations:
        if number % 2 == 0:
            key = f'Teklar {number}'
        else:
            key = f'Human {number}'
        result[key] = name
    return result