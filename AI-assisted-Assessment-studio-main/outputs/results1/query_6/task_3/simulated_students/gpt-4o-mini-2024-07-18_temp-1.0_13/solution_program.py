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
        with open(filename, 'w') as f:
            powers_str = ','.join(self.powers)
            f.write(f'{self.name},{self.creature_type},{self.origin},{powers_str}')

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = f.read().strip().split(',')
            name = data[0]
            creature_type = data[1]
            origin = data[2]
            powers = data[3].split('')
            return cls(name, creature_type, origin, powers)

# Test Cases
if __name__ == '__main__':
    # Creating an instance
    creature = MythicalCreature('Phoenix', 'Bird', 'Fire', ['Rebirth', 'Flight', 'Fire Control'])

    # Describe the creature
    print(creature.describe())  # 'Phoenix is a Bird from Fire. Powers: Rebirth, Flight, Fire Control'

    # Save to file
    creature.save_to_file('creature.txt')

    # Load from file
    loaded_creature = MythicalCreature.load_from_file('creature.txt')

    # Describe the loaded creature
    print(loaded_creature.describe())  # Should match the original description