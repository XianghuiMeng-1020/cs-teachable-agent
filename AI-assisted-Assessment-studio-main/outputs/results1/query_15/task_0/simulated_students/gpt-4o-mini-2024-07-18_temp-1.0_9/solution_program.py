def can_teleport_sequence(nodes, connections):
    # Create a graph from connections
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    # Check each consecutive teleportation request
    for i in range(len(nodes) - 1):
        if nodes[i] not in graph or nodes[i + 1] not in graph[nodes[i]]:
            return False
    return True