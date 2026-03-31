def can_teleport_sequence(nodes, connections):
    # Create a graph from the connections
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    # Check teleportation requests consecutively
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        if current_node not in graph or next_node not in graph[current_node]:
            return False
    return True