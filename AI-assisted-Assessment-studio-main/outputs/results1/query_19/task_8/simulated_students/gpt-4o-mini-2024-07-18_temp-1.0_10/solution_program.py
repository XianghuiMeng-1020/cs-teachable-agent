def log_position(timestamp, x, y):
    try:
        with open('navigation_log.txt', 'a') as file:
            file.write(f'{timestamp}, {x}, {y}\n')
    except Exception as e:
        print(f'Error logging position: {e}')


def retrieve_positions():
    positions = []
    try:
        with open('navigation_log.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    timestamp = parts[0].strip()
                    x = int(parts[1].strip())
                    y = int(parts[2].strip())
                    positions.append({'timestamp': timestamp, 'x': x, 'y': y})
    except FileNotFoundError:
        return positions  # Return empty list if file does not exist
    except Exception as e:
        print(f'Error retrieving positions: {e}')
    return positions