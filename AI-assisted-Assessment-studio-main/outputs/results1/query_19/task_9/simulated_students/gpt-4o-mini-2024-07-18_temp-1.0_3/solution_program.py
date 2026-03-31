import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    file_pattern = "star_log_"
    
    try:
        for filename in os.listdir(directory):
            if filename.startswith(file_pattern) and filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, 'r') as file:
                        for line in file:
                            if event_type in line:
                                collected_entries.append(line.strip())
                except (IOError, OSError):
                    continue
    except (IOError, OSError):
        return
    
    try:
        with open(output_file, 'w') as out_file:
            for entry in collected_entries:
                out_file.write(entry + '\n')
    except (IOError, OSError):
        return