def can_teleport_sequence(nodes, connections):
    # Create a dictionary to hold all connections
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    # Check if each node in the sequence can be reached from the previous one
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        # If current_node has no outgoing connections, return False
        if current_node not in graph:
            return False
        # Check if the next_node is reachable from current_node
        if next_node not in graph[current_node]:
            return False

    return True