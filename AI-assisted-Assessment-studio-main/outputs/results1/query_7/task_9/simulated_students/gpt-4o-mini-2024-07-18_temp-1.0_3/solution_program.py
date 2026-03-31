def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if '-' in line:
                title, description = line.split('-', 1)
                title = title.strip()
                description = description.strip()
                reversed_title = ' '.join(word.upper() for word in title.split()[::-1])
                reversed_description = ' '.join(word.upper() for word in description.split()[::-1])
                outfile.write(f'{reversed_title} - {reversed_description}\n')