def calculate_crystal_weights(mining_data):
    glimmer_weight = 0
    shadow_weight = 0
    for weight in mining_data:
        if weight % 2 == 0:
            glimmer_weight += weight
        else:
            shadow_weight += weight
    return (glimmer_weight, shadow_weight)