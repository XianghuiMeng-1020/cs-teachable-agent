def process_records(input_file, output_file):
    count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if ',' in line:
                date, description = line.split(',', 1)
                try:
                    year, month, day = map(int, date.split('-'))
                    if 1 <= month <= 12 and 1 <= day <= 31:
                        outfile.write(line + '\n')
                        count += 1
                except ValueError:
                    continue
    return count