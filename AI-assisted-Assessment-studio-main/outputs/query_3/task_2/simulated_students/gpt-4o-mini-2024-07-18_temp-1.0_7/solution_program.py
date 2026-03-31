def calculate_efficiency(messages: dict) -> dict:
    efficiencies = {}
    for station, connections in messages.items():
        total_messages = sum(connections.values())
        id_sum = sum(ord(char) for char in station)
        if id_sum > 0:
            efficiency_score = total_messages / id_sum
            efficiencies[station] = round(efficiency_score, 2)
        else:
            efficiencies[station] = 0.00
    return efficiencies