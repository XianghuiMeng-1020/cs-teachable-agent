def calculate_crystal_weights(mining_data):
    glimmer_total = 0
    shadow_total = 0
    
    for weight in mining_data:
        if weight % 2 == 0:
            glimmer_total += weight
        else:
            shadow_total += weight
    
    return (glimmer_total, shadow_total)

# Example usage:
# print(calculate_crystal_weights([4, 9, 6, 3, 10, 15, 2]))  # Output: (22, 27)