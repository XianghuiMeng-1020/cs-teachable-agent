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

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            data = file.read().strip().split(',')
            name = data[0]
            creature_type = data[1]
            origin = data[2]
            powers = data[3:]
            return MythicalCreature(name, creature_type, origin, powers)

# Test cases
creature = MythicalCreature('Dragon', 'Fire', 'Legends', ['Fire Breathing', 'Flight'])
assert creature.describe() == 'Dragon is a Fire from Legends. Powers: Fire Breathing, Flight'
creature.save_to_file('dragon.txt')
loaded_creature = MythicalCreature.load_from_file('dragon.txt')
assert loaded_creature.describe() == 'Dragon is a Fire from Legends. Powers: Fire Breathing, Flight'