def get_strengthiest_beast(filename):
    max_strength = -1
    strengthiest_beast = ""
    with open(filename, 'r') as file:
        for line in file:
            creature, strength = line.strip().split(',')
            strength = int(strength)
            if strength > max_strength:
                max_strength = strength
                strengthiest_beast = creature
    return strengthiest_beast
