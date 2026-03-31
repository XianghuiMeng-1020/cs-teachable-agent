def calculate_dish_time(dish_times):
    total_time = 0
    for entry in dish_times:
        try:
            total_time += int(entry)
        except (ValueError, TypeError):
            pass
    return total_time
