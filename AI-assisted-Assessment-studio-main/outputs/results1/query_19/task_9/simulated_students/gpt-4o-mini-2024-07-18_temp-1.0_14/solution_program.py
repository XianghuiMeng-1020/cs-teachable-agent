import os

def parse_logs(directory, event_type, output_file):
    log_entries = []
    
    for filename in os.listdir(directory):
        if filename.startswith("star_log_") and filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if event_type in line:
                            log_entries.append(line.strip())
            except (FileNotFoundError, IOError):
                continue
    
    with open(output_file, 'w') as out_file:
        for entry in log_entries:
            out_file.write(entry + '\n')