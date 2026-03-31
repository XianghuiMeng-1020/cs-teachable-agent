def calculate_dish_time(dish_times):
    total_time = 0
    for time in dish_times:
        try:
            total_time += int(time)
        except (ValueError, TypeError):
            pass
    return total_time