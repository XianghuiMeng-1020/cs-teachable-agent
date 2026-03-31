def calculate_average_cooking_time(file_path):
    try:
        with open(file_path, 'r') as file:
            total_time = 0
            count = 0
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            time = int(parts[1].strip())
                            total_time += time
                            count += 1
                        except ValueError:
                            continue
            if count == 0:
                raise ValueError("No valid cooking times found")
            return round(total_time / count, 2)
    except FileNotFoundError:
        raise FileNotFoundError