def calculate_average_cooking_time(file_path):
    total_time = 0
    count = 0
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        dish, time_str = parts
                        try:
                            time = float(time_str)
                            total_time += time
                            count += 1
                        except ValueError:
                            continue
        
    except FileNotFoundError:
        raise FileNotFoundError()
    
    if count == 0:
        raise ValueError("No valid cooking times found")
    
    average_time = total_time / count
    return round(average_time, 2)