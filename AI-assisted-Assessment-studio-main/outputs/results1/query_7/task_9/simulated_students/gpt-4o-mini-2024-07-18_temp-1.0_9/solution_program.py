def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if ' - ' in line:
                title, description = line.split(' - ', 1)
                title = ' '.join(reversed(title.strip().split())).upper()
                description = ' '.join(reversed(description.strip().split())).upper()
                outfile.write(f'{title} - {description}\n')