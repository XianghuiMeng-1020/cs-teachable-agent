import datetime


def process_records(input_file, output_file):
    valid_record_count = 0
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line.count(',') == 1:
                    date_str, description = line.split(',', 1)
                    date_str = date_str.strip()
                    description = description.strip()
                    try:
                        datetime.datetime.strptime(date_str, '%Y-%m-%d')
                        outfile.write(f'{date_str}, {description}\n')
                        valid_record_count += 1
                    except ValueError:
                        continue
    except IOError:
        pass  
    
    return valid_record_count