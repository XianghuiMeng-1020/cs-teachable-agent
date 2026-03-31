def can_teleport_sequence(nodes, connections):
    # Create a dictionary to store the teleportation connections
    teleport_map = {}
    for a, b in connections:
        if a not in teleport_map:
            teleport_map[a] = []
        teleport_map[a].append(b)

    # Check if we can make each teleportation in the sequence
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        # Check if there is a direct connection from current_node to next_node
        if current_node not in teleport_map or next_node not in teleport_map[current_node]:
            return False

    return True