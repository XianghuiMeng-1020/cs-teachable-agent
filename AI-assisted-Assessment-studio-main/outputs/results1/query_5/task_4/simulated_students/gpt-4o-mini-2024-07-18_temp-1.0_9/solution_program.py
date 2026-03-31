def get_strengthiest_beast(filename):
    strongest_beast = ""
    max_strength = -1
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            creature = parts[0]
            strength = int(parts[1])
            if strength > max_strength:
                max_strength = strength
                strongest_beast = creature
    return strongest_beast
