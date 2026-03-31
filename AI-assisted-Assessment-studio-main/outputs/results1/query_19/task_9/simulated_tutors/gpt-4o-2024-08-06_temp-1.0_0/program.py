import os

# Function to parse logs
def parse_logs(directory, event_type, output_file):
    # List to store matching log entries
    matching_entries = []
    
    # Iterate over every file in the directory
    for filename in os.listdir(directory):
        if filename.startswith('star_log_') and filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            
            try:
                with open(filepath, 'r') as file:
                    # Read each line in the file
                    for line in file:
                        # Check if the line contains the given event type
                        if event_type in line:
                            matching_entries.append(line)
            except Exception as e:
                # Handle any exception (e.g., file not found or read error) by skipping the file
                continue
    
    # Write all matching entries to the output file
    try:
        with open(output_file, 'w') as outfile:
            outfile.writelines(matching_entries)
    except Exception as e:
        # Handle exception if any during file writing
        print(f"An error occurred while writing to the file: {e}")