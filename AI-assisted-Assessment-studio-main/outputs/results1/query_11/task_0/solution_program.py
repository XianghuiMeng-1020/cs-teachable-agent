def calculate_ingredients(recipe_list, recipe_name):
    for recipe in recipe_list:
        if recipe[0] == recipe_name:
            ingredients = []
            for ingredient in recipe[1]:
                found = False
                for i, (ingr_name, qty) in enumerate(ingredients):
                    if ingr_name == ingredient[0]:
                        ingredients[i] = (ingr_name, qty + ingredient[1])
                        found = True
                        break
                if not found:
                    ingredients.append(ingredient)
            return ingredients
    return []