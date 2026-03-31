import os


def parse_logs(directory, event_type, output_file):
    log_entries = []
    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    for line in file:
                        if event_type in line:
                            log_entries.append(line.strip())
            except (FileNotFoundError, IOError):
                continue

    # Write collected entries to the output file
    with open(output_file, 'w') as output:
        for entry in log_entries:
            output.write(entry + '\n')
