def calculate_efficiency(messages: dict) -> dict:
    efficiency_scores = {}
    
    for station, connections in messages.items():
        total_messages = sum(connections.values())
        sum_id = sum(ord(char) for char in station)
        efficiency_score = total_messages / sum_id if sum_id != 0 else 0
        efficiency_scores[station] = round(efficiency_score, 2)
    
    return efficiency_scores