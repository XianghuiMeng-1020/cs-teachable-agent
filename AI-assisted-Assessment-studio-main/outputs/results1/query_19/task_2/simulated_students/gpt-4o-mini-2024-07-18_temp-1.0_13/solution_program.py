import os

def read_log_file(file_path):
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, 'r') as file:
            log_entries = []
            for line in file:
                if line.strip():
                    timestamp, event_description = line.split(' - ', 1)
                    log_entries.append((timestamp, event_description.strip()))
            # Sort the log entries by timestamp
            log_entries.sort(key=lambda x: x[0])
            return [event[1] for event in log_entries]
    except (IOError, ValueError):
        return []