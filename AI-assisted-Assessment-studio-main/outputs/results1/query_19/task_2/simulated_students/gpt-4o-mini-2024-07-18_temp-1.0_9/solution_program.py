def read_log_file(file_path):
    import os
    from datetime import datetime

    if not os.path.isfile(file_path):
        return []

    events = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    timestamp, description = parts[0], parts[1]
                    event_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    events.append((event_time, description))
    except (IOError, ValueError):
        return []

    events.sort(key=lambda x: x[0])
    return [description for _, description in events]