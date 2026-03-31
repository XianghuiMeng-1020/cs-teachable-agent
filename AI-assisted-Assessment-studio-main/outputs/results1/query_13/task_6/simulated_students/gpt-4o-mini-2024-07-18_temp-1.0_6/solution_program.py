def process_ingredient_usage(file_path):
    ingredient_usage = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            if len(parts) != 2:
                continue
            ingredient, amount = parts
            
            try:
                amount = int(amount)
            except ValueError:
                continue
            
            if ingredient in ingredient_usage:
                ingredient_usage[ingredient] += amount
            else:
                ingredient_usage[ingredient] = amount
    
    return ingredient_usage