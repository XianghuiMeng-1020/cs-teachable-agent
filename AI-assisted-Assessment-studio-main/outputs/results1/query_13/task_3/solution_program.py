def cook_recipe(ingredients, available):
    try:
        results = []
        for item in ingredients:
            name, quantity = item
            if name not in available:
                results.append(f"{name}: Missing")
            else:
                if available[name] >= quantity:
                    results.append(f"{name}: Enough")
                else:
                    difference = quantity - available[name]
                    results.append(f"{name}: Not Enough, {difference} grams more needed")
        return results
    except:
        return 'Error'