def log_position(timestamp, x, y):
    try:
        with open('navigation_log.txt', 'a') as f:
            f.write(f'{timestamp}, {x}, {y}\n')
    except Exception as e:
        print(f'Error logging position: {e}')


def retrieve_positions():
    positions = []
    try:
        with open('navigation_log.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(', ')
                if len(parts) == 3:
                    timestamp, x, y = parts
                    positions.append({
                        'timestamp': timestamp,
                        'x': int(x),
                        'y': int(y)
                    })
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f'Error retrieving positions: {e}')
    return positions