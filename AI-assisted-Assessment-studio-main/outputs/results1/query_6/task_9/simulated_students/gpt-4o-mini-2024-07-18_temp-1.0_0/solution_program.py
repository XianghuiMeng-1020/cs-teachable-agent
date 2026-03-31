class MythicalLibrary:
    def __init__(self, filename='mythical_creatures.txt'):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = [x.strip() for x in line.split(',', 2)]
                    creatures[name.lower()] = {'origin': origin, 'description': description}
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create the file if it doesn't exist
        return creatures

    def get_description(self, creature_name):
        creature_name_lower = creature_name.lower()
        if creature_name_lower in self.creatures:
            return self.creatures[creature_name_lower]['description']
        return 'Creature not found'

    def add_creature(self, creature_name, origin, description):
        creature_name_lower = creature_name.lower()
        if creature_name_lower in self.creatures:
            return 'Creature already exists'
        with open(self.filename, 'a') as file:
            file.write(f'{creature_name}, {origin}, {description}\n')
        self.creatures[creature_name_lower] = {'origin': origin, 'description': description}

    def get_creatures_by_origin(self, origin):
        return [name for name, info in self.creatures.items() if info['origin'].lower() == origin.lower()]