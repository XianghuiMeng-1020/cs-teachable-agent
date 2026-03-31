import os


def parse_logs(directory, event_type, output_file):
    log_lines = []
    
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as file:
                    for line in file:
                        if event_type in line:
                            log_lines.append(line.strip())
            except Exception as e:
                continue

    with open(output_file, 'w') as outfile:
        for log in log_lines:
            outfile.write(log + '\n')
