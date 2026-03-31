def calculate_efficiency(messages: dict) -> dict:
    efficiency_scores = {}
    
    for station_id, connections in messages.items():
        total_messages = sum(connections.values())
        id_sum = sum(ord(char) for char in station_id)
        efficiency_scores[station_id] = round(total_messages / id_sum, 2)
    
    return efficiency_scores