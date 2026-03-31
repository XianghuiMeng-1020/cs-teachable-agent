def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not lines:  # Check if the file is empty
            with open('stats.txt', 'w') as f:
                f.write('0.00\nNone\n0')
            return

        total_power = 0
        creature_count = 0
        max_power = float('-inf')
        creature_with_max_power = None

        for line in lines:
            if line.strip():  # Ignore empty lines
                parts = line.rsplit(' ', 1)  # Split into name and power
                creature_name = parts[0]
                power = int(parts[1])

                # Arithmetic operations
                total_power += power
                creature_count += 1

                if power > max_power:  # Comparison with possible selection
                    max_power = power
                    creature_with_max_power = creature_name

        average_power = total_power / creature_count if creature_count > 0 else 0

        # Writing output to a file
        with open('stats.txt', 'w') as f:
            f.write(f"{average_power:.2f}\n{creature_with_max_power}\n{creature_count}")

    except (FileNotFoundError, IOError):
        with open('stats.txt', 'w') as f:
            f.write('0.00\nNone\n0')