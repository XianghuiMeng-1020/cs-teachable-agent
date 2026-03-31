import datetime


def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def process_records(input_file, output_file):
    valid_count = 0
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_str, description = line.split(',', 1)
                    if is_valid_date(date_str):
                        outfile.write(line + '\n')
                        valid_count += 1
    except IOError:
        pass
    return valid_count