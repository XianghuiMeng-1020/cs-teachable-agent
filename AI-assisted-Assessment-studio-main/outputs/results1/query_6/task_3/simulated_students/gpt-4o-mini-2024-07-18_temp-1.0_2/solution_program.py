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
            file.write(f'{self.name},{self.creature_type},{self.origin},{powers_str}\n')

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            name, creature_type, origin, powers_str = line.split(',')
            powers = powers_str.split(',')
            return cls(name, creature_type, origin, powers)

# Test cases
creature1 = MythicalCreature('Dragon', 'Fire', 'Mythology', ['Flight', 'Fire Breathing'])
assert creature1.describe() == 'Dragon is a Fire from Mythology. Powers: Flight, Fire Breathing'

creature1.save_to_file('creature1.txt')

creature_loaded = MythicalCreature.load_from_file('creature1.txt')
assert creature_loaded.name == 'Dragon'
assert creature_loaded.creature_type == 'Fire'
assert creature_loaded.origin == 'Mythology'
assert creature_loaded.powers == ['Flight', 'Fire Breathing']