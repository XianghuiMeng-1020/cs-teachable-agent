def get_strengthiest_beast(filename):
    max_strength = -1
    strongest_beast = ""
    with open(filename, 'r') as file:
        for line in file:
            name, strength = line.split(',')
            strength = int(strength.strip())
            if strength > max_strength:
                max_strength = strength
                strongest_beast = name.strip()
    return strongest_beast
