def sort_space_stations(stations):
    sorted_stations = {}
    for number in sorted(stations.keys()):
        if number % 2 == 0:
            prefix = 'Teklar '
        else:
            prefix = 'Human '
        sorted_stations[prefix + str(number)] = stations[number]
    return sorted_stations