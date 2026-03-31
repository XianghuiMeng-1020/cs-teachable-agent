def read_log_file(file_path):
    import os
    from datetime import datetime
    events = []
    
    try:
        if not os.path.isfile(file_path):
            return []
        
        with open(file_path, 'r') as file:
            for line in file:
                if '-' in line:
                    timestamp, event_description = line.split(' - ', 1)
                    timestamp = datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
                    events.append((timestamp, event_description.strip()))
        
        events.sort(key=lambda x: x[0])
        return [event for _, event in events]
    except Exception:
        return []