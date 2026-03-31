def sort_space_stations(stations):
    sorted_stations = dict()
    for number in sorted(stations.keys()):
        if number % 2 == 0:
            prefix = 'Teklar'
        else:
            prefix = 'Human'
        new_key = f'{prefix} {number}'
        sorted_stations[new_key] = stations[number]
    return sorted_stations