def can_teleport_sequence(nodes, connections):
    # Create a dictionary to represent the graph of connections
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    # Check if all requested teleportations can be made consecutively
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        # If the current node is not in the graph or it cannot reach the next node
        if current_node not in graph or next_node not in graph[current_node]:
            return False
    return True