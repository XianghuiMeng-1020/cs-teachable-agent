class SpaceCargo:
    def __init__(self):
        self.inventory = {}

    def add_item(self, name, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if name in self.inventory:
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

    def remove_item(self, name, quantity):
        if name not in self.inventory:
            raise KeyError(f"Item '{name}' not found in inventory.")
        if self.inventory[name] < quantity:
            raise KeyError(f"Insufficient quantity for item '{name}'.")
        self.inventory[name] -= quantity
        if self.inventory[name] == 0:
            del self.inventory[name]

    def get_item_quantity(self, name):
        return self.inventory.get(name, 0)

    def list_items(self):
        return sorted(self.inventory.keys())