def process_ingredient_usage(file_path):
    inventory = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                ingredient, amount = line.split(':')
                amount = int(amount)
                ingredient = ingredient.strip()
                if ingredient in inventory:
                    inventory[ingredient] += amount
                else:
                    inventory[ingredient] = amount
            except (ValueError, TypeError):
                continue
    return inventory