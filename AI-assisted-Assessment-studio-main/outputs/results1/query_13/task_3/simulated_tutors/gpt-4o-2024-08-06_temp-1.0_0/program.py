def cook_recipe(ingredients, available):
    status_list = []
    try:
        for ingredient, required_qty in ingredients:
            if isinstance(required_qty, int):
                available_qty = available.get(ingredient, None)
                if available_qty is None:
                    status_list.append(f"{ingredient}: Missing")
                elif available_qty >= required_qty:
                    status_list.append(f"{ingredient}: Enough")
                else:
                    shortage = required_qty - available_qty
                    status_list.append(f"{ingredient}: Not Enough, {shortage} grams more needed")
            else:
                return 'Error'
        return status_list
    except Exception:
        return 'Error'