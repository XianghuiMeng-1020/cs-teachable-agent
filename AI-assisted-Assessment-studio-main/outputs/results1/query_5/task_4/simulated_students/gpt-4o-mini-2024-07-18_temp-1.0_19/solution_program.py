def get_strengthiest_beast(filename):
    try:
        with open(filename, 'r') as file:
            strongest_beast = None
            max_strength = -1
            for line in file:
                name, strength = line.strip().split(',')
                strength = int(strength)
                if strength > max_strength:
                    max_strength = strength
                    strongest_beast = name
            return strongest_beast if strongest_beast else ''
    except FileNotFoundError:
        return ''

if __name__ == '__main__':
    result = get_strengthiest_beast('mythological_beasts.txt')
    print(result)