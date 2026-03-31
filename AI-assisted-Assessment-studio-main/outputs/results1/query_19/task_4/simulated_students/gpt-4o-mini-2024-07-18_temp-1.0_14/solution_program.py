import re
from datetime import datetime


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def process_records(input_file, output_file):
    valid_record_count = 0
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_part, description_part = line.split(',', 1)
                    date_part = date_part.strip()
                    description_part = description_part.strip()
                    
                    if is_valid_date(date_part) and description_part:
                        outfile.write(line + '\n')
                        valid_record_count += 1
    except IOError:
        print('An error occurred while handling files.')
        
    return valid_record_count