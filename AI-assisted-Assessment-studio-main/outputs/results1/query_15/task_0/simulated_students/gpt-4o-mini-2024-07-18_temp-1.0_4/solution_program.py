def can_teleport_sequence(nodes, connections):
    # Create a dictionary to hold connections for quick lookup
    teleport_map = {}
    for a, b in connections:
        if a not in teleport_map:
            teleport_map[a] = []
        teleport_map[a].append(b)

    # Check if we can move through all nodes in the sequence
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        if current_node not in teleport_map or next_node not in teleport_map[current_node]:
            return False

    return True