class Spaceship:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.inventory = {}

    def add_item(self, name, category, weight):
        total_weight = self.total_weight()
        if name in self.inventory:
            # Update existing item
            current_item = self.inventory[name]
            total_weight -= current_item['weight']  # Remove current item's weight
        
        if total_weight + weight > self.capacity:
            raise Exception("Insufficient capacity")

        self.inventory[name] = {'category': category, 'weight': weight}

    def remove_item(self, name):
        if name not in self.inventory:
            raise Exception("Item not found")
        del self.inventory[name]

    def total_weight(self):
        weight = sum(item['weight'] for item in self.inventory.values())
        return weight

    def list_items(self):
        return [(name, item['category'], item['weight']) for name, item in self.inventory.items()]