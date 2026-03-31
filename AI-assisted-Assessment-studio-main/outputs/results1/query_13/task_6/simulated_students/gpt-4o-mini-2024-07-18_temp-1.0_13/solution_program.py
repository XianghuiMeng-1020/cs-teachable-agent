def process_ingredient_usage(file_path):
    inventory = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    ingredient = parts[0].strip()
                    try:
                        amount = int(parts[1].strip())
                        if ingredient in inventory:
                            inventory[ingredient] += amount
                        else:
                            inventory[ingredient] = amount
                    except ValueError:
                        continue
    return inventory