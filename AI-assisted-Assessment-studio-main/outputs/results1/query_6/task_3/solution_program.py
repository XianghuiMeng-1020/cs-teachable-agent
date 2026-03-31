class MythicalCreature:
    def __init__(self, name, creature_type, origin, powers):
        self.name = name
        self.creature_type = creature_type
        self.origin = origin
        self.powers = powers

    def describe(self):
        powers_string = ', '.join(self.powers)
        return f'{self.name} is a {self.creature_type} from {self.origin}. Powers: {powers_string}'

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            powers_string = ','.join(self.powers)
            f.write(f'{self.name},{self.creature_type},{self.origin},{powers_string}\n')

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = f.readline().strip()
            name, creature_type, origin, *powers = data.split(',')
            return cls(name, creature_type, origin, powers)