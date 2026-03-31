def log_position(timestamp, x, y):
    try:
        with open('navigation_log.txt', 'a') as file:
            file.write(f"{timestamp}, {x}, {y}\n")
    except IOError:
        pass


def retrieve_positions():
    positions = []
    if not os.path.exists('navigation_log.txt'):
        return positions
    try:
        with open('navigation_log.txt', 'r') as file:
            for line in file:
                segments = line.strip().split(', ')
                if len(segments) == 3:
                    positions.append({'timestamp': segments[0], 'x': int(segments[1]), 'y': int(segments[2])})
    except IOError:
        pass
    return positions