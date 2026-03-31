class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        name = parts[0].strip().lower()
                        origin = parts[1].strip()
                        description = parts[2].strip()
                        creatures[name] = (origin, description)
        except FileNotFoundError:
            open(self.filename, 'w').close()  # create file if doesn't exist
        return creatures

    def get_description(self, creature_name):
        creature_name = creature_name.strip().lower()
        if creature_name in self.creatures:
            return self.creatures[creature_name][1]
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        creature_name = creature_name.strip().lower()
        if creature_name in self.creatures:
            return "Creature already exists"
        self.creatures[creature_name] = (origin, description)
        with open(self.filename, 'a') as file:
            file.write(f"{creature_name.capitalize()}, {origin}, {description}\n")
        return "Creature added"

    def get_creatures_by_origin(self, origin):
        origin = origin.strip().lower()
        return [name.capitalize() for name, (orig, _) in self.creatures.items() if orig.lower() == origin]