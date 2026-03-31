import os


def parse_logs(directory, event_type, output_file):
    log_entries = []
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as file:
                    for line in file:
                        if line.strip().startswith(event_type + ':'):
                            log_entries.append(line.strip())
            except Exception:
                continue
    with open(output_file, 'w') as outfile:
        for entry in log_entries:
            outfile.write(entry + '\n')