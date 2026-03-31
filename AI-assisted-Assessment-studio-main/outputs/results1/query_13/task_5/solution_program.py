def calculate_average_cooking_time(file_path):
    total_time = 0
    count = 0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    try:
                        total_time += int(parts[1])
                        count += 1
                    except ValueError:
                        continue
        if count == 0:
            raise ValueError("No valid cooking times found")
        return round(total_time / count, 2)
    except FileNotFoundError:
        raise FileNotFoundError