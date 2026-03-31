def process_ingredient_usage(file_path):
    ingredient_dict = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines
                
            try:
                ingredient, amount = line.split(':', 1)  # split only on the first colon
                amount = int(amount)
                ingredient = ingredient.strip()
                
                if ingredient in ingredient_dict:
                    ingredient_dict[ingredient] += amount
                else:
                    ingredient_dict[ingredient] = amount
            except (ValueError, IndexError):
                continue  # skip lines with errors
                
    return ingredient_dict