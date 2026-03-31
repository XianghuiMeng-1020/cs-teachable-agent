import os

class KitchenInventory:
    def __init__(self, filename):
        self.filename = filename
        self.inventory = {}
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    ingredient, quantity = line.strip().split(':')
                    self.inventory[ingredient] = int(quantity)
        else:
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