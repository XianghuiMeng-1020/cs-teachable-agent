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

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            name, creature_type, origin, powers_str = line.split(',')
            powers = powers_str.split(',')
            return cls(name, creature_type, origin, powers)

# Test cases
if __name__ == '__main__':
    # Creating an instance
    dragon = MythicalCreature('Dragon', 'Fire Creature', 'China', ['Flying', 'Breathing Fire', 'Immortality'])
    # Describing the creature
    print(dragon.describe())
    # Saving the creature data
    dragon.save_to_file('dragon.txt')
    # Loading the creature from the file
    loaded_dragon = MythicalCreature.load_from_file('dragon.txt')
    # Describing the loaded creature
    print(loaded_dragon.describe())