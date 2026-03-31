def can_teleport_sequence(nodes, connections):
    # Create a set to store the connections as a directed graph
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)

    # Check if we can teleport through the nodes in sequence
    for i in range(len(nodes) - 1):
        if nodes[i] not in graph or nodes[i + 1] not in graph[nodes[i]]:
            return False

    return True