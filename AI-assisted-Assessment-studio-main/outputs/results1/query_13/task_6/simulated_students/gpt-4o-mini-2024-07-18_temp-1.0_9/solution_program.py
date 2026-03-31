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
            ingredient, usage_str = parts
            try:
                usage = int(usage_str)
                if ingredient in ingredient_usage:
                    ingredient_usage[ingredient] += usage
                else:
                    ingredient_usage[ingredient] = usage
            except ValueError:
                continue
    return ingredient_usage