import os


def get_recipes_by_category(filename, category_name):
    recipes = []
    
    if not os.path.isfile(filename):
        return recipes
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                fields = line.split(';')
                
                if len(fields) != 4:
                    continue  # Skip invalid lines
                
                recipe_name = fields[0].strip()
                ingredients = fields[1].strip()
                prep_time = fields[2].strip()
                category = fields[3].strip()
                
                if category.lower() == category_name.lower():
                    recipes.append(recipe_name)
    except Exception:
        return recipes
    
    return recipes