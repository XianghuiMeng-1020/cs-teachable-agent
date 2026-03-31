class Spaceship:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.inventory = {}

    def add_item(self, name, category, weight):
        # Check if the item exists to update it
        if name in self.inventory:
            current_weight = self.total_weight() - self.inventory[name]['weight']
        else:
            current_weight = self.total_weight()

        # Check for sufficient capacity
        if current_weight + weight > self.capacity:
            raise Exception("Insufficient capacity")

        # Add or update the item
        self.inventory[name] = {'category': category, 'weight': weight}

    def remove_item(self, name):
        if name not in self.inventory:
            raise Exception("Item not found")
        del self.inventory[name]

    def total_weight(self):
        return sum(item['weight'] for item in self.inventory.values())

    def list_items(self):
        return [(name, details['category'], details['weight']) 
                for name, details in self.inventory.items()]