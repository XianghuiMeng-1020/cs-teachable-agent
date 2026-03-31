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
            data = file.read().strip().split(',')
            name = data[0]
            creature_type = data[1]
            origin = data[2]
            powers = data[3:]
            return cls(name, creature_type, origin, powers)

# Test cases to ensure functionality
if __name__ == '__main__':
    dragon = MythicalCreature('Falkor', 'Dragon', 'Fantasia', ['Flying', 'Fire Breath', 'Luck'])
    print(dragon.describe())  # Expected description output
    dragon.save_to_file('dragon.txt')
    loaded_dragon = MythicalCreature.load_from_file('dragon.txt')
    print(loaded_dragon.describe())  # Expected description output should match the original