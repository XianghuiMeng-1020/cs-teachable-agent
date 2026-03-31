def can_teleport_sequence(nodes, connections):
    connection_map = {}
    
    for a, b in connections:
        if a not in connection_map:
            connection_map[a] = set()
        connection_map[a].add(b)
    
    for i in range(len(nodes) - 1):
        start_node = nodes[i]
        end_node = nodes[i + 1]
        if start_node not in connection_map or end_node not in connection_map[start_node]:
            return False
    
    return True