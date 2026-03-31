import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    for line in file:
                        if event_type in line:
                            collected_entries.append(line.strip())
            except Exception as e:
                continue
    with open(output_file, 'w') as out_file:
        for entry in collected_entries:
            out_file.write(entry + '\n')