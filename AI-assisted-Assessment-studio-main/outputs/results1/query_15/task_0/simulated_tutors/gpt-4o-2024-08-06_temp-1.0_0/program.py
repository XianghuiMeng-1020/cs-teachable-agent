def can_teleport_sequence(nodes, connections):
    # Create a set of tuples for quick lookup of connections
    connection_set = set(connections)
    
    # Iterate over the nodes list and check for each teleportation
    for i in range(len(nodes) - 1):
        source = nodes[i]
        destination = nodes[i + 1]
        
        # If there's no direct connection between consecutive nodes, return False
        if (source, destination) not in connection_set:
            return False
    
    # If all connections are valid, return True
    return True

# Example tests:
print(can_teleport_sequence([1, 2, 3], [(1, 2), (2, 3)])) # True
print(can_teleport_sequence([1, 2, 3], [(1, 3), (3, 2)])) # False
