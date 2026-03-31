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
            powers_string = ','.join(self.powers)
            file.write(f'{self.name},{self.creature_type},{self.origin},{powers_string}')

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = file.readline().strip().split(',')
            name = data[0]
            creature_type = data[1]
            origin = data[2]
            powers = data[3].split(';')
            return cls(name, creature_type, origin, powers)

# Example test cases
creature1 = MythicalCreature('Phoenix', 'Bird', 'Egypt', ['Rebirth', 'Fire', 'Healing'])
print(creature1.describe())
creature1.save_to_file('creature1.txt')

creature2 = MythicalCreature.load_from_file('creature1.txt')
print(creature2.describe())