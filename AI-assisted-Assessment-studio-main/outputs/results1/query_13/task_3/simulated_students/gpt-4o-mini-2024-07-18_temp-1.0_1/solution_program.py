def cook_recipe(ingredients, available):
    status_list = []
    
    for ingredient, required in ingredients:
        try:
            if ingredient not in available:
                status_list.append(f"{ingredient}: Missing")
            else:
                available_weight = available[ingredient]
                if available_weight >= required:
                    status_list.append(f"{ingredient}: Enough")
                else:
                    status_list.append(f"{ingredient}: Not Enough, {required - available_weight} grams more needed")
        except Exception:
            return 'Error'
    
    return status_list