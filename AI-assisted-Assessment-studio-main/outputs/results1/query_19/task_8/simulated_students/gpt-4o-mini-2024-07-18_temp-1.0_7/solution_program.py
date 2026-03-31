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
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    ts, x, y = line.strip().split(', ')
                    positions.append({'timestamp': ts, 'x': int(x), 'y': int(y)})
    except FileNotFoundError:
        return positions
    except Exception as e:
        print(f'Error retrieving positions: {e}')
    return positions