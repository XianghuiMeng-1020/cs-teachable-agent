class AlienRegistry:
    def __init__(self):
        self.species_registry = {}

    def add_species(self, species_name, characteristics):
        if species_name in self.species_registry:
            raise ValueError(f'Species {species_name} already exists')
        self.species_registry[species_name] = characteristics

    def get_species_info(self, species_name):
        if species_name not in self.species_registry:
            raise ValueError('Species not found')
        return self.species_registry[species_name]

    def get_all_species(self):
        return sorted(self.species_registry.keys())