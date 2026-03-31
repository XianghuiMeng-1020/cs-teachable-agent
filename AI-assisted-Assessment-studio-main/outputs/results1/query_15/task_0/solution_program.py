def can_teleport_sequence(nodes, connections):
    for i in range(len(nodes) - 1):
        found = False
        for connection in connections:
            if connection[0] == nodes[i] and connection[1] == nodes[i+1]:
                found = True
                break
        if not found:
            return False
    return True
