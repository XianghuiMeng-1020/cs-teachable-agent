def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if '-' in line:
                title, description = line.split('-', 1)
                title = title.strip()
                description = description.strip()
                title_reversed = ' '.join(reversed(title.split()))
                description_reversed = ' '.join(reversed(description.split()))
                title_upper = title_reversed.upper()
                description_upper = description_reversed.upper()
                outfile.write(f'{title_upper} - {description_upper}\n')