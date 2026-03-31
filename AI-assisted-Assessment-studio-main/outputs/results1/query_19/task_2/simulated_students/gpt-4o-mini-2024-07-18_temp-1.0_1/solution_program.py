def read_log_file(file_path):
    import os
    import datetime

    if not os.path.isfile(file_path):
        return []

    event_entries = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '-' in line:
                    timestamp, event_description = line.split(' - ', 1)
                    event_entries.append((datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), event_description.strip()))

        event_entries.sort(key=lambda x: x[0])
        return [event[1] for event in event_entries]
    except (IOError, ValueError):
        return []