def calculate_efficiency(messages):
    efficiency_scores = {}
    for station, connections in messages.items():
        total_messages = sum(connections.values())
        id_value = sum(ord(char) for char in station)
        efficiency = total_messages / id_value if id_value != 0 else 0
        efficiency_scores[station] = round(efficiency, 2)
    for station in messages.keys() - efficiency_scores.keys():
        efficiency_scores[station] = 0.0
    return efficiency_scores