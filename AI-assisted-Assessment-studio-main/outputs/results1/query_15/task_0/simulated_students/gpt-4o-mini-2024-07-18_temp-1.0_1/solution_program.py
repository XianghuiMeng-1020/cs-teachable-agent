def can_teleport_sequence(nodes, connections):
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)
    for i in range(len(nodes) - 1):
        start = nodes[i]
        end = nodes[i + 1]
        if start not in graph or end not in graph[start]:
            return False
    return True