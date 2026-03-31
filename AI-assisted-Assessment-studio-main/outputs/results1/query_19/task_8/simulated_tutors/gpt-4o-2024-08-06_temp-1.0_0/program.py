import os


def log_position(timestamp, x, y):
    """
    Logs the spaceship's position in the navigation_log.txt file.

    Args:
    - timestamp (str): The timestamp at which the position is recorded.
    - x (int): The x coordinate of the spaceship's position.
    - y (int): The y coordinate of the spaceship's position.
    """
    try:
        with open('navigation_log.txt', 'a') as file:
            file.write(f"{timestamp}, {x}, {y}\n")  # Append a new line with the position
    except Exception as e:
        print("Failed to log position:", e)


def retrieve_positions():
    """
    Retrieves all logged positions from navigation_log.txt.

    Returns:
    - List of dictionaries with keys 'timestamp', 'x', 'y'.
    """
    positions = []
    if not os.path.exists('navigation_log.txt'):
        return positions

    try:
        with open('navigation_log.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Check if line is not empty
                    parts = line.split(', ')
                    if len(parts) == 3:
                        timestamp, x, y = parts[0], int(parts[1]), int(parts[2])
                        positions.append({'timestamp': timestamp, 'x': x, 'y': y})
    except Exception as e:
        print("Error retrieving positions:", e)

    return positions