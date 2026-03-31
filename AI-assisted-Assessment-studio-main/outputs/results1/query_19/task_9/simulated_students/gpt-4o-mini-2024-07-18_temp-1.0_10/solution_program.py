import os


def parse_logs(directory, event_type, output_file):
    logs = []
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    for line in file:
                        if f'{event_type}:' in line:
                            logs.append(line.strip())
            except Exception:
                continue
    try:
        with open(output_file, 'w') as output_file_handle:
            for log in logs:
                output_file_handle.write(log + '\n')
    except Exception:
        pass
