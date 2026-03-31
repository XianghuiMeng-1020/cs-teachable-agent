class KitchenInventory:
    def __init__(self, filename):
        self.filename = filename
        self.inventory = {}
    
    def load_inventory(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    ingredient, quantity = line.strip().split(':')
                    self.inventory[ingredient] = int(quantity)
        except FileNotFoundError:
            # Start with empty inventory if no file found
            self.inventory = {}
    
    def check_availability(self, ingredient):
        return ingredient in self.inventory and self.inventory[ingredient] > 0
    
    def add_ingredient(self, ingredient, quantity):
        if ingredient in self.inventory:
            self.inventory[ingredient] += quantity
        else:
            self.inventory[ingredient] = quantity

    def save_inventory(self):
        with open(self.filename, 'w') as file:
            for ingredient, quantity in self.inventory.items():
                file.write(f'{ingredient}:{quantity}\n')

# Evaluating context relevance
# This task heavily involves using classes and objects (`KitchenInventory` class), file handling and I/O (methods `load_inventory` and `save_inventory`),
# selection statements (exception handling and `check_availability`), variables (ingredient and quantity management). Thus, the theme and concepts are relevant.
context_relevance = 1