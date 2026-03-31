import os
from datetime import datetime


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def process_records(input_file, output_file):
    valid_records_count = 0
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if ',' in line:
                    date_part, desc_part = line.split(',', 1)
                    if is_valid_date(date_part.strip()):
                        outfile.write(line + '\n')
                        valid_records_count += 1
    except IOError as e:
        print(f"An error occurred: {e}")
    return valid_records_count

# Example usage
# count = process_records('zog_records.txt', 'valid_zog_records.txt')
# print(f"Number of valid records: {count}")