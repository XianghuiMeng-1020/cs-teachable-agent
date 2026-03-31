import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    # Iterate through the files in the given directory
    for filename in os.listdir(directory):
        # Check if the file matches the naming pattern
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        # If the line contains the specified event type, collect it
                        if event_type in line:
                            collected_entries.append(line.strip())
            except (IOError, OSError):
                continue  # Skip the file if an error occurs

    # Write the collected entries to the output file
    with open(output_file, 'w') as out_file:
        for entry in collected_entries:
            out_file.write(entry + '\n')