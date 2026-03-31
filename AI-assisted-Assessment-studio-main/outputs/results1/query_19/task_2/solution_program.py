def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            entries = []
            for line in file:
                line = line.strip()
                if line:
                    date_part, event = line.split(' - ', 1)
                    entries.append((date_part, event))
            entries.sort()
            return [event for _, event in entries]
    except (IOError, FileNotFoundError):
        return []