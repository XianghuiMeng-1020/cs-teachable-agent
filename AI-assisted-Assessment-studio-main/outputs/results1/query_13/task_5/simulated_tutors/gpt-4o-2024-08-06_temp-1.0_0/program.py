def calculate_average_cooking_time(file_path):
    total_time = 0
    valid_count = 0
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and split by comma
                parts = line.strip().split(',')
                
                if len(parts) == 2:
                    try:
                        # Convert the cooking time to integer
                        dish_name, cooking_time_str = parts
                        cooking_time = int(cooking_time_str)
                        total_time += cooking_time
                        valid_count += 1
                    except ValueError:
                        # Skip lines where the cooking time is not a valid integer
                        continue
        
        # Ensure we return an average only if we have at least one valid cooking time
        if valid_count == 0:
            raise ValueError("No valid cooking times found")

        # Calculate and return the average
        average_time = total_time / valid_count
        return round(average_time, 2)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e