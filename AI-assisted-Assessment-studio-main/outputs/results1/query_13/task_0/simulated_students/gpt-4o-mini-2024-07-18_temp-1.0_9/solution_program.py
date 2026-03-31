def calculate_dish_time(dish_times):
    total_time = 0
    for time in dish_times:
        if isinstance(time, (int, str)):
            try:
                total_time += int(time)
            except ValueError:
                pass
    return total_time