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
            file.write(f'{self.name},{self.creature_type},{self.origin},{powers_string}\n')

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            name, creature_type, origin, powers_string = line.split(',')
            powers = powers_string.split(',')
            return cls(name, creature_type, origin, powers)

# Test cases
# Creating instances
creature1 = MythicalCreature('Dragon', 'Serpent', 'China', ['Fire Breath', 'Flying'])
creature2 = MythicalCreature('Unicorn', 'Horse', 'Europe', ['Healing', 'Invisibility'])

# Describing creatures
assert creature1.describe() == 'Dragon is a Serpent from China. Powers: Fire Breath, Flying'
assert creature2.describe() == 'Unicorn is a Horse from Europe. Powers: Healing, Invisibility'

# Saving to file
creature1.save_to_file('creature1.txt')
creature2.save_to_file('creature2.txt')

# Loading from file
loaded_creature1 = MythicalCreature.load_from_file('creature1.txt')
loaded_creature2 = MythicalCreature.load_from_file('creature2.txt')

# Asserting loaded data
assert loaded_creature1.describe() == creature1.describe()
assert loaded_creature2.describe() == creature2.describe()