def calculate_efficiency(messages: dict) -> dict:
    efficiency_scores = {}
    
    for station, connections in messages.items():
        total_messages = sum(connections.values())
        id_sum = sum(ord(char) for char in station)
        efficiency_score = round(total_messages / id_sum, 2) if id_sum > 0 else 0.00
        efficiency_scores[station] = efficiency_score
    
    return efficiency_scores