def sort_space_stations(stations):
    sorted_stations = { ("Human " + str(k) if k % 2 != 0 else "Teklar " + str(k)) : v for k, v in sorted(stations.items()) }
    return sorted_stations