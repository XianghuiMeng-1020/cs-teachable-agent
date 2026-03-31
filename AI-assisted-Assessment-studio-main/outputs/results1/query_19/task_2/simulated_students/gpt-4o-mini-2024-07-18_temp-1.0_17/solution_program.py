import os
from datetime import datetime

def read_log_file(file_path):
    if not os.path.isfile(file_path):
        return []
    
    entries = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split(' - ', 1)
                if len(parts) == 2:
                    timestamp_str = parts[0]  
                    event_description = parts[1].strip()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    entries.append((timestamp, event_description))
        entries.sort(key=lambda x: x[0])
        return [event[1] for event in entries]
    except (IOError, ValueError):
        return []