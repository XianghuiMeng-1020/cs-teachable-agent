import re

def is_valid_date(date_str):
    date_pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
    match = date_pattern.match(date_str)
    if match:
        year, month, day = map(int, match.groups())
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
    return False

def process_records(input_file, output_file):
    valid_record_count = 0
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_str, description = line.split(',', 1)
                    if is_valid_date(date_str.strip()):
                        outfile.write(line + '\n')
                        valid_record_count += 1
    except IOError:
        pass
    return valid_record_count