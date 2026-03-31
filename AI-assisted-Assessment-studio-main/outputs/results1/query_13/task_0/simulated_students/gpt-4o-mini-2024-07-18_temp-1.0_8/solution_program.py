def calculate_dish_time(dish_times):
    total_time = 0
    for item in dish_times:
        try:
            total_time += int(item)
        except (ValueError, TypeError):
            continue
    return total_time