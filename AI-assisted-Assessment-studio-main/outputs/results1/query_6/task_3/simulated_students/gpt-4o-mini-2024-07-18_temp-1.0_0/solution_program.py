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
        powers_str = ','.join(self.powers)
        with open(filename, 'w') as file:
            file.write(f'{self.name},{self.creature_type},{self.origin},{powers_str}')

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            name, creature_type, origin, powers_str = line.split(',')
            powers = powers_str.split(',')
            return MythicalCreature(name, creature_type, origin, powers)

# Test cases
creature1 = MythicalCreature('Phoenix', 'Bird', 'Fire', ['Immortal', 'Rebirth'])
assert creature1.describe() == 'Phoenix is a Bird from Fire. Powers: Immortal, Rebirth'

creature1.save_to_file('creature1.txt')
creature2 = MythicalCreature.load_from_file('creature1.txt')
assert creature2.name == 'Phoenix'
assert creature2.creature_type == 'Bird'
assert creature2.origin == 'Fire'
assert creature2.powers == ['Immortal', 'Rebirth']