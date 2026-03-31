class Spaceship:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.inventory = {}

    def add_item(self, name, category, weight):
        if name in self.inventory:
            current_weight = self.inventory[name]['weight']
            new_weight = current_weight - weight
            if new_weight + self.total_weight() > self.capacity:
                raise Exception("Insufficient capacity")
            self.inventory[name] = {'category': category, 'weight': weight}
        else:
            if self.total_weight() + weight > self.capacity:
                raise Exception("Insufficient capacity")
            self.inventory[name] = {'category': category, 'weight': weight}

    def remove_item(self, name):
        if name in self.inventory:
            del self.inventory[name]
        else:
            raise Exception("Item not found")

    def total_weight(self):
        return sum(item['weight'] for item in self.inventory.values())

    def list_items(self):
        return [(name, item['category'], item['weight']) for name, item in self.inventory.items()]