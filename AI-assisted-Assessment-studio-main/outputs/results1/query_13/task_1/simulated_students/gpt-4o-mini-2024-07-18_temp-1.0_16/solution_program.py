def estimate_cooking_time(dish_list):
    total_time = 0
    for dish in dish_list:
        if not isinstance(dish, str):
            raise ValueError('Invalid item in dish list')
        total_time += len(dish) * 5
    return total_time