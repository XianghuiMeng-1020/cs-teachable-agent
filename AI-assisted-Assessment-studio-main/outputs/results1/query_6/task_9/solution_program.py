class MythicalLibrary:
    def __init__(self):
        self.filename = 'mythical_creatures.txt'
        with open(self.filename, 'r') as file:
            self.creatures = [line.strip() for line in file]

    def get_description(self, creature_name):
        creature_name = creature_name.lower()
        for creature in self.creatures:
            name, _, description = creature.split(', ', 2)
            if name.lower() == creature_name:
                return description
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        creature_name = creature_name.lower()
        for creature in self.creatures:
            name, _, _ = creature.split(', ', 2)
            if name.lower() == creature_name:
                return "Creature already exists"
        new_entry = f"{creature_name.title()}, {origin}, {description}"
        self.creatures.append(new_entry)
        with open(self.filename, 'a') as file:
            file.write(new_entry + "\n")

    def get_creatures_by_origin(self, origin):
        origin = origin.lower()
        return [creature.split(', ', 1)[0] for creature in self.creatures if creature.split(', ', 2)[1].lower() == origin]