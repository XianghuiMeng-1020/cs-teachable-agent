def log_position(timestamp, x, y):
    try:
        with open('navigation_log.txt', 'a') as log_file:
            log_file.write(f'{timestamp}, {x}, {y}\n')
    except Exception as e:
        print(f'Error logging position: {e}')


def retrieve_positions():
    positions = []
    try:
        with open('navigation_log.txt', 'r') as log_file:
            for line in log_file:
                parts = line.strip().split(', ')
                if len(parts) == 3:
                    timestamp = parts[0]
                    x = int(parts[1])
                    y = int(parts[2])
                    positions.append({'timestamp': timestamp, 'x': x, 'y': y})
    except FileNotFoundError:
        return positions
    except Exception as e:
        print(f'Error retrieving positions: {e}')
    return positions