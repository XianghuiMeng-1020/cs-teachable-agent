def process_ingredient_usage(file_path):
    ingredient_usage = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                ingredient, usage = line.split(':', 1)
                ingredient = ingredient.strip()
                usage = usage.strip()
                try:
                    usage_amount = int(usage)
                    if ingredient in ingredient_usage:
                        ingredient_usage[ingredient] += usage_amount
                    else:
                        ingredient_usage[ingredient] = usage_amount
                except ValueError:
                    continue  # Ignore non-integer usage
    return ingredient_usage