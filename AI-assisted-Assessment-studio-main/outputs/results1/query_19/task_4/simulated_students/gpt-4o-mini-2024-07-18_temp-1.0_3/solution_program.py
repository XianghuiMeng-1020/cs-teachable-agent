import re
from datetime import datetime

def process_records(input_file, output_file):
    valid_records_count = 0
    date_pattern = re.compile("^\d{4}-\d{2}-\d{2}$")
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_str, description = line.split(',', 1)
                    if date_pattern.match(date_str):
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            outfile.write(line + '\n')
                            valid_records_count += 1
                        except ValueError:
                            continue
    except IOError:
        pass
    return valid_records_count