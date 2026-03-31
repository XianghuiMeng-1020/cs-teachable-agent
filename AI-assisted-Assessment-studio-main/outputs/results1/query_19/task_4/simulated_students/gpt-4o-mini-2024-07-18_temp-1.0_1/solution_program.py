from datetime import datetime


def process_records(input_file, output_file):
    valid_record_count = 0
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Strip whitespace characters
                line = line.strip()
                # Check for exactly one comma
                if line.count(',') == 1:
                    date_str, description = line.split(',', 1)
                    # Validate date format
                    try:
                        datetime.strptime(date_str.strip(), '%Y-%m-%d')
                        # If valid, write to output file
                        outfile.write(line + '\n')
                        valid_record_count += 1
                    except ValueError:
                        continue  # Invalid date format

    except IOError:
        pass  # Handle file read/write errors gracefully

    return valid_record_count