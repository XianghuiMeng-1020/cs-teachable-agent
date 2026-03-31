class Spaceship:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.inventory = {}

    def add_item(self, name, category, weight):
        current_weight = self.total_weight()
        if current_weight + weight > self.capacity:
            raise Exception("Insufficient capacity")
        self.inventory[name] = {'category': category, 'weight': weight}

    def remove_item(self, name):
        if name not in self.inventory:
            raise Exception("Item not found")
        del self.inventory[name]

    def total_weight(self):
        return sum(item['weight'] for item in self.inventory.values())

    def list_items(self):
        return [(name, info['category'], info['weight']) for name, info in self.inventory.items()]