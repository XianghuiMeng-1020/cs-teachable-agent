import os


def parse_logs(directory, event_type, output_file):
    collected_entries = []
    
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        # Check if the file name matches the expected pattern
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                # Open the file and read lines
                with open(file_path, 'r') as file:
                    for line in file:
                        # Check if the line contains the specified event type
                        if event_type in line:
                            collected_entries.append(line.strip())
            except (FileNotFoundError, IOError):
                continue  # Skip the file if there's an error
    
    # Write collected entries to the output file
    try:
        with open(output_file, 'w') as output:
            for entry in collected_entries:
                output.write(entry + '\n')
    except (FileNotFoundError, IOError):
        pass  # Handle output file errors gracefully