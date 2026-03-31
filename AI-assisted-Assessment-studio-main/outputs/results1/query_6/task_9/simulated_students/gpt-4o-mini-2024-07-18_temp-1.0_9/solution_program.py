class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    name, origin, description = line.strip().split(', ', 2)
                    creatures[name.lower()] = (origin, description)
        except FileNotFoundError:
            open(self.filename, 'w').close()  # create the file if it does not exist
        return creatures

    def get_description(self, creature_name):
        creature_name = creature_name.lower()
        if creature_name in self.creatures:
            return self.creatures[creature_name][1]
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        creature_name = creature_name.lower()
        if creature_name in self.creatures:
            return "Creature already exists"
        self.creatures[creature_name] = (origin, description)
        with open(self.filename, 'a') as f:
            f.write(f'{creature_name}, {origin}, {description}\n')
        return "Creature added"

    def get_creatures_by_origin(self, origin):
        origin = origin.lower()
        return [name for name, (o, _) in self.creatures.items() if o.lower() == origin]