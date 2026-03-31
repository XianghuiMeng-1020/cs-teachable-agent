def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            title_description = line.split('-', 1)
            if len(title_description) == 2:
                title = title_description[0].strip()
                description = title_description[1].strip()
                processed_title = ' '.join(reversed(title.split())).upper()
                processed_description = ' '.join(reversed(description.split())).upper()
                outfile.write(f'{processed_title} - {processed_description}\n')