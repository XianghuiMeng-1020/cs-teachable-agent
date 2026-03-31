def can_teleport_sequence(nodes, connections):
    # Create a dictionary to represent the graph
    teleport_graph = {}
    for a, b in connections:
        if a not in teleport_graph:
            teleport_graph[a] = []
        teleport_graph[a].append(b)

    # Iterate through the nodes to check teleportation connections
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        # Check if there is a connection from current_node to next_node
        if current_node not in teleport_graph or next_node not in teleport_graph[current_node]:
            return False

    return True