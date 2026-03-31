class MythicalCreature:
    def __init__(self, name, creature_type, origin, powers):
        self.name = name
        self.creature_type = creature_type
        self.origin = origin
        self.powers = powers

    def describe(self):
        powers_list = ', '.join(self.powers)
        return f'{self.name} is a {self.creature_type} from {self.origin}. Powers: {powers_list}'

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            powers_str = ','.join(self.powers)
            file.write(f'{self.name},{self.creature_type},{self.origin},{powers_str}')

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            name, creature_type, origin, powers_str = line.split(',')
            powers = powers_str.split(',')
            return MythicalCreature(name, creature_type, origin, powers)

