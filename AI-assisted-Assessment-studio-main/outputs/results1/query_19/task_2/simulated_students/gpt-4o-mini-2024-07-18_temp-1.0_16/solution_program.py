import os

from datetime import datetime


def read_log_file(file_path):
    if not os.path.isfile(file_path):
        return []
    
    entries = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into timestamp and the event description
                if ' - ' in line:
                    timestamp, event = line.split(' - ', 1)
                    try:
                        # Parse the timestamp and append to entries
                        timestamp_dt = datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
                        entries.append((timestamp_dt, event.strip()))
                    except ValueError:
                        continue  # Skip lines with invalid timestamp format
    except Exception:
        return []
    
    # Sort entries by timestamp
    entries.sort(key=lambda x: x[0])
    
    # Extract sorted event descriptions
    sorted_events = [event for _, event in entries]
    
    return sorted_events