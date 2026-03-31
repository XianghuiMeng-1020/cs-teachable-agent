import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    log_file_pattern = r'star_log_\d+\.txt'
    
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if line.split()[1].rstrip(':') == event_type:
                            collected_entries.append(line.strip())
            except (FileNotFoundError, IOError) as e:
                continue  # Skip the file on error
                
    with open(output_file, 'w') as output:
        for entry in collected_entries:
            output.write(entry + '\n')