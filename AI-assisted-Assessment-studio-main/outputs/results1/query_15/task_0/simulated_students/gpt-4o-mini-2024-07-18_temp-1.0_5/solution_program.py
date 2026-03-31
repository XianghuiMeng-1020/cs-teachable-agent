def can_teleport_sequence(nodes, connections):
    teleport_map = {}
    
    for a, b in connections:
        if a not in teleport_map:
            teleport_map[a] = set()
        teleport_map[a].add(b)
    
    for i in range(len(nodes) - 1):
        if nodes[i] not in teleport_map or nodes[i + 1] not in teleport_map[nodes[i]]:
            return False
    
    return True