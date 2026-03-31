import os

class KitchenInventory:
    def __init__(self, filename):
        self.filename = filename
        self.inventory = {}
        self.load_inventory()

    def load_inventory(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    ingredient, quantity = line.strip().split(':')
                    self.inventory[ingredient] = int(quantity)
        except Exception as e:
            print(f"Error loading inventory: {e}")

    def check_availability(self, ingredient):
        return ingredient in self.inventory and self.inventory[ingredient] > 0

    def add_ingredient(self, ingredient, quantity):
        if ingredient in self.inventory:
            self.inventory[ingredient] += quantity
        else:
            self.inventory[ingredient] = quantity

    def save_inventory(self):
        try:
            with open(self.filename, 'w') as file:
                for ingredient, quantity in self.inventory.items():
                    file.write(f"{ingredient}:{quantity}\n")
        except Exception as e:
            print(f"Error saving inventory: {e}")