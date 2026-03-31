def can_teleport_sequence(nodes, connections):
    # Create a dictionary for faster lookups of teleportation connections
    teleport_map = {}
    for a, b in connections:
        if a not in teleport_map:
            teleport_map[a] = set()
        teleport_map[a].add(b)

    # Check each pair of consecutive nodes in the requested sequence
    for i in range(len(nodes) - 1):
        from_node = nodes[i]
        to_node = nodes[i + 1]
        # Check if a teleport is possible from from_node to to_node
        if from_node not in teleport_map or to_node not in teleport_map[from_node]:
            return False

    return True