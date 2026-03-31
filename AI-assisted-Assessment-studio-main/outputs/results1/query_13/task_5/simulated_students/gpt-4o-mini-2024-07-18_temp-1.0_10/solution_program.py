def calculate_average_cooking_time(file_path):
    cooking_times = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            time = int(parts[1].strip())
                            cooking_times.append(time)
                        except ValueError:
                            continue
    except FileNotFoundError:
        raise FileNotFoundError

    if not cooking_times:
        raise ValueError("No valid cooking times found")

    average_time = sum(cooking_times) / len(cooking_times)
    return round(average_time, 2)