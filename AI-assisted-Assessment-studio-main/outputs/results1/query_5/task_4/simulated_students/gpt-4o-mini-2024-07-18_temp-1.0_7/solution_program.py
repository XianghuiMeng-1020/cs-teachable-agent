def get_strengthiest_beast(filename):
    strengthiest_name = ''
    max_strength = -1
    with open(filename, 'r') as file:
        for line in file:
            name, strength = line.strip().split(',')
            strength = int(strength)
            if strength > max_strength:
                max_strength = strength
                strengthiest_name = name
    return strengthiest_name
