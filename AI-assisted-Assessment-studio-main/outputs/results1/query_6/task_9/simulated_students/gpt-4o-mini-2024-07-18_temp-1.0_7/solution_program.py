class MythicalLibrary:
    def __init__(self, filename='mythical_creatures.txt'):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = line.strip().split(',', 2)
                    creatures[name.strip().lower()] = (origin.strip(), description.strip())
        except FileNotFoundError:
            pass
        return creatures

    def get_description(self, creature_name):
        key = creature_name.strip().lower()
        if key in self.creatures:
            origin, description = self.creatures[key]
            return description
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        key = creature_name.strip().lower()
        if key not in self.creatures:
            self.creatures[key] = (origin.strip(), description.strip())
            with open(self.filename, 'a') as file:
                file.write(f'{creature_name}, {origin}, {description}\n')
            return
        return "Creature already exists"

    def get_creatures_by_origin(self, origin):
        return [name for name, (orig, _) in self.creatures.items() if orig.lower() == origin.strip().lower()]