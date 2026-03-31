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
            ingredient, usage = parts
            try:
                usage_amount = int(usage)
                if ingredient in ingredient_usage:
                    ingredient_usage[ingredient] += usage_amount
                else:
                    ingredient_usage[ingredient] = usage_amount
            except ValueError:
                continue
    
    return ingredient_usage