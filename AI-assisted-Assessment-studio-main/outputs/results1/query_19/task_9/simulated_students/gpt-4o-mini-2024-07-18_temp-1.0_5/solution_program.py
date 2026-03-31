import os


def parse_logs(directory, event_type, output_file):
    log_entries = []
    
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if line.startswith(event_type + ':'):
                            log_entries.append(line.strip())
            except (IOError, OSError):
                continue
    
    with open(output_file, 'w') as outfile:
        for entry in log_entries:
            outfile.write(entry + '\n')
