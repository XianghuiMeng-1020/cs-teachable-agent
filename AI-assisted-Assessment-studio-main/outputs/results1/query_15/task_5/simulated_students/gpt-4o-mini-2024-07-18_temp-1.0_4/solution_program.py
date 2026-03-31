def calculate_crystal_weights(mining_data):
    glimmer_weight = sum(weight for weight in mining_data if weight % 2 == 0)
    shadow_weight = sum(weight for weight in mining_data if weight % 2 != 0)
    return (glimmer_weight, shadow_weight)