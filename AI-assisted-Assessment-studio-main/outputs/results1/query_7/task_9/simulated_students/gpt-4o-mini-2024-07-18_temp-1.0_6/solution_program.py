def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            title_description = line.split('-')
            if len(title_description) != 2:
                continue
            title = title_description[0].strip()
            description = title_description[1].strip()
            reversed_title = ' '.join(reversed(title.split())).upper()
            reversed_description = ' '.join(reversed(description.split())).upper()
            outfile.write(f'{reversed_title} - {reversed_description}\n')