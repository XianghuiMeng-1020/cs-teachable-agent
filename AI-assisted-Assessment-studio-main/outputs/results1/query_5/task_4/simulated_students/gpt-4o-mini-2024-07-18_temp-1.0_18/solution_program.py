def get_strengthiest_beast(filename):
    max_strength = 0
    strongest_beast = ''
    with open(filename, 'r') as file:
        for line in file:
            name, strength = line.strip().split(',')
            strength = int(strength)
            if strength > max_strength:
                max_strength = strength
                strongest_beast = name
    return strongest_beast

if __name__ == '__main__':
    print(get_strengthiest_beast('mythological_beasts.txt'))