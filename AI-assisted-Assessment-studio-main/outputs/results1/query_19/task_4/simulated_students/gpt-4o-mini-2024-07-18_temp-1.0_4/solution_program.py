import datetime


def process_records(input_file, output_file):
    valid_record_count = 0
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_part, description_part = line.split(',', 1)
                    date_part = date_part.strip()
                    if validate_date(date_part):
                        outfile.write(line + '\n')
                        valid_record_count += 1
    except IOError:
        pass  # Gracefully handle file IO exceptions
    
    return valid_record_count


def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
