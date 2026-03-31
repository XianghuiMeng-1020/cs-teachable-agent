class Creature:
    def __init__(self, name, origin, description):
        self.name = name
        self.origin = origin
        self.description = description

    def __str__(self):
        return f'{self.name}, {self.origin}, {self.description}'


def read_creatures_from_file(file_path):
    creatures = []
    with open(file_path, 'r') as file:
        for line in file:
            name, origin, description = line.strip().split(',')
            creatures.append(Creature(name, origin, description))
    return creatures


def save_creatures_to_file(creatures, file_path):
    with open(file_path, 'w') as file:
        for creature in creatures:
            file.write(str(creature) + '\n')


input_file = 'creatures.txt'
output_file = 'output_creatures.txt'
creatures = read_creatures_from_file(input_file)
save_creatures_to_file(creatures, output_file)