def calculate_average_cooking_time(file_path):
    try:
        with open(file_path, 'r') as file:
            cooking_times = []
            for line in file:
                line = line.strip()
                if line:  # Ignore empty lines
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            cooking_time = float(parts[1])  # Convert cooking time to float
                            cooking_times.append(cooking_time)
                        except ValueError:
                            continue  # Ignore lines with invalid cooking times

            if not cooking_times:
                raise ValueError("No valid cooking times found")

            average_time = sum(cooking_times) / len(cooking_times)
            return round(average_time, 2)
    except FileNotFoundError:
        raise FileNotFoundError("The specified file was not found")