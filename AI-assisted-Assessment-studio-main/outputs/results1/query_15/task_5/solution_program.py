def calculate_crystal_weights(mining_data):
    glimmer_total = 0
    shadow_total = 0
    for ore in mining_data:
        if ore % 2 == 0:
            glimmer_total += ore
        else:
            shadow_total += ore
    return (glimmer_total, shadow_total)