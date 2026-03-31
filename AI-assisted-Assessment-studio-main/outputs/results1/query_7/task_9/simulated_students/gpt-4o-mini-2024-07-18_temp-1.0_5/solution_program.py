def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if '-' in line:
                title, description = line.split('-', 1)
                title = title.strip()
                description = description.strip()
                processed_title = ' '.join(reversed(title.upper().split()))
                processed_description = ' '.join(reversed(description.upper().split()))
                outfile.write(f'{processed_title} - {processed_description}\n')