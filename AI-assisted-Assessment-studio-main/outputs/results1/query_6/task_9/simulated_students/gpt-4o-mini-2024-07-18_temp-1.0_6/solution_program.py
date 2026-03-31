class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = [item.strip() for item in line.split(',')]
                    creatures[name.lower()] = {'origin': origin, 'description': description}
        except FileNotFoundError:
            pass
        return creatures

    def get_description(self, creature_name):
        creature_name = creature_name.lower()
        if creature_name in self.creatures:
            return self.creatures[creature_name]['description']
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        creature_name = creature_name.lower()
        if creature_name in self.creatures:
            return "Creature already exists"
        self.creatures[creature_name] = {'origin': origin, 'description': description}
        with open(self.filename, 'a') as file:
            file.write(f'{creature_name.capitalize()}, {origin}, {description}\n')

    def get_creatures_by_origin(self, origin):
        return [name.capitalize() for name, info in self.creatures.items() if info['origin'].lower() == origin.lower()]