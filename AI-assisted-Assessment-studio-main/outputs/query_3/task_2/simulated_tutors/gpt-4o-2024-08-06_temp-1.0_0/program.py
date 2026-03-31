def calculate_efficiency(messages: dict) -> dict:
    efficiencies = {}
    for station, connections in messages.items():
        total_messages = sum(connections.values())
        id_sum = sum(ord(char) for char in station)
        efficiency = total_messages / id_sum if id_sum != 0 else 0
        efficiencies[station] = round(efficiency, 2)
    return efficiencies

# Example usage:
messages1 = {
    'Alpha-1': {'Beta-2': 100, 'Delta-4': 250},
    'Beta-2': {'Alpha-1': 50},
    'Delta-4': {'Alpha-1': 100, 'Beta-2': 150}
}
result = calculate_efficiency(messages1)
print(result)