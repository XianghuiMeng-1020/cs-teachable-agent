import os


def parse_logs(directory, event_type, output_file):
    collected_logs = []
    
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if event_type in line:
                            collected_logs.append(line.strip())
            except (FileNotFoundError, IOError):
                continue
    
    with open(output_file, 'w') as output_file:
        for log in collected_logs:
            output_file.write(log + '\n')