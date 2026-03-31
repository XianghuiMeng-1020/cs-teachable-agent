def calculate_average_cooking_time(file_path):
    try:
        with open(file_path, 'r') as file:
            total_time = 0
            dish_count = 0
            for line in file:
                line = line.strip()
                if line:  
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            cooking_time = float(parts[1].strip())
                            total_time += cooking_time
                            dish_count += 1
                        except ValueError:
                            continue
            if dish_count == 0:
                raise ValueError("No valid cooking times found")
            average_time = total_time / dish_count
            return round(average_time, 2)
    except FileNotFoundError:
        raise FileNotFoundError