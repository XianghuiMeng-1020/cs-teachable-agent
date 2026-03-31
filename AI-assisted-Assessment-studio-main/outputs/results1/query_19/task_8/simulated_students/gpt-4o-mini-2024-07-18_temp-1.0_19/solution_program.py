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
                parts = line.strip().split(', ')
                position = {
                    'timestamp': parts[0],
                    'x': int(parts[1]),
                    'y': int(parts[2])
                }
                positions.append(position)
    except FileNotFoundError:
        return positions
    except Exception as e:
        print(f'Error retrieving positions: {e}')
    return positions