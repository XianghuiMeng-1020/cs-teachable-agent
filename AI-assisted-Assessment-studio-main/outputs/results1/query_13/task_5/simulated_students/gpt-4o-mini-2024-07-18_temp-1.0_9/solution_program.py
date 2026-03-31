def calculate_average_cooking_time(file_path):
    try:
        with open(file_path, 'r') as file:
            total_cooking_time = 0
            num_dishes = 0
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            cooking_time = float(parts[1])
                            total_cooking_time += cooking_time
                            num_dishes += 1
                        except ValueError:
                            continue

            if num_dishes == 0:
                raise ValueError("No valid cooking times found")

            return round(total_cooking_time / num_dishes, 2)
    except FileNotFoundError:
        raise FileNotFoundError()