def calculate_efficiency(messages: dict) -> dict:
    efficiencies = {}

    for station, connections in messages.items():
        total_messages = sum(connections.values())
        id_sum = sum(ord(char) for char in station)
        efficiency_score = total_messages / id_sum if id_sum != 0 else 0
        efficiencies[station] = round(efficiency_score, 2)

    return efficiencies