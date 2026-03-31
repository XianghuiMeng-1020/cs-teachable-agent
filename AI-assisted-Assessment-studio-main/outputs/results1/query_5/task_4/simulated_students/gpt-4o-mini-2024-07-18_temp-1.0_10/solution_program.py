def get_strengthiest_beast(filename):
    strengthiest_beast = ''
    max_strength = -1
    with open(filename, 'r') as file:
        for line in file:
            name, strength = line.strip().split(',')
            strength = int(strength)
            if strength > max_strength:
                max_strength = strength
                strengthiest_beast = name
    return strengthiest_beast

if __name__ == '__main__':
    print(get_strengthiest_beast('mythological_beasts.txt'))