def calculate_dish_time(dish_times):
    total_time = 0
    for time in dish_times:
        if isinstance(time, int):
            total_time += time
        elif isinstance(time, str):
            try:
                total_time += int(time)
            except ValueError:
                continue
    return total_time