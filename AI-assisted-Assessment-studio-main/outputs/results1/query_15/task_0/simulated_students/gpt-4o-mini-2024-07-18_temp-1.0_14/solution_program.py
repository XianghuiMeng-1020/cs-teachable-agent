def can_teleport_sequence(nodes, connections):
    teleport_map = {}
    for start, end in connections:
        if start not in teleport_map:
            teleport_map[start] = set()  
        teleport_map[start].add(end)

    for i in range(len(nodes) - 1):
        current = nodes[i]
        next_node = nodes[i + 1]
        if current not in teleport_map or next_node not in teleport_map[current]:
            return False
    return True