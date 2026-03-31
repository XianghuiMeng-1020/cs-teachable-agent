def can_teleport_sequence(nodes, connections):
    connection_map = {}
    for a, b in connections:
        if a not in connection_map:
            connection_map[a] = set()
        connection_map[a].add(b)

    for i in range(len(nodes) - 1):
        if nodes[i] not in connection_map or nodes[i + 1] not in connection_map[nodes[i]]:
            return False
    return True