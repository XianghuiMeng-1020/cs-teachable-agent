def calculate_ingredients(recipe_list, recipe_name):
    for recipe in recipe_list:
        if recipe[0] == recipe_name:
            ingredient_dict = {}
            for ingredient, quantity in recipe[1]:
                if ingredient in ingredient_dict:
                    ingredient_dict[ingredient] += quantity
                else:
                    ingredient_dict[ingredient] = quantity
            return list(ingredient_dict.items())
    return []

# Test the function with a basic recipe list
recipe_list = [ 
    ("Pasta", [("Flour", 100), ("Egg", 2), ("Salt", 1)]),
    ("Omelette", [("Egg", 3), ("Salt", 1), ("Oil", 1)]),
    ("Cake", [("Flour", 200), ("Egg", 3), ("Sugar", 100), ("Salt", 1)])
]

# Example usage
print(calculate_ingredients(recipe_list, "Cake"))
# Output: [('Flour', 200), ('Egg', 3), ('Sugar', 100), ('Salt', 1)]