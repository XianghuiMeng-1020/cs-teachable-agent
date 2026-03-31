def calculate_average_cooking_time(file_path):
    try:
        with open(file_path, 'r') as file:
            cooking_times = []
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            time = float(parts[1])
                            cooking_times.append(time)
                        except ValueError:
                            continue
        if not cooking_times:
            raise ValueError("No valid cooking times found")
        average_time = sum(cooking_times) / len(cooking_times)
        return round(average_time, 2)
    except FileNotFoundError:
        raise FileNotFoundError