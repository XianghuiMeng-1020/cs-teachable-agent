import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    for line in file:
                        if line.startswith(event_type + ':'):
                            collected_entries.append(line.strip())
            except (FileNotFoundError, IOError):
                continue  # Skip this file on error
    
    with open(output_file, 'w') as outfile:
        for entry in collected_entries:
            outfile.write(entry + '\n')