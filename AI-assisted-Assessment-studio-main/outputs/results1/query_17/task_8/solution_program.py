class AlienRegistry:
    def __init__(self):
        self.registry = {}

    def add_species(self, species_name, characteristics):
        if species_name not in self.registry:
            self.registry[species_name] = characteristics

    def get_species_info(self, species_name):
        if species_name in self.registry:
            return self.registry[species_name]
        else:
            raise ValueError("Species not found")

    def get_all_species(self):
        return sorted(self.registry.keys())