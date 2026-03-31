import re

def validate_date(date_string):
    pattern = r'\d{4}-\d{2}-\d{2}'
    return bool(re.match(pattern, date_string))

def process_records(input_file, output_file):
    valid_record_count = 0
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_part, description_part = line.split(',', 1)
                    if validate_date(date_part.strip()):
                        outfile.write(line + '\n')
                        valid_record_count += 1
    except IOError:
        pass  
    return valid_record_count
