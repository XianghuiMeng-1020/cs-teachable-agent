def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if '-' in line:
                title, description = line.split('-', 1)
                title = title.strip().split()[::-1]
                description = description.strip().split()[::-1]
                processed_title = ' '.join(word.upper() for word in title)
                processed_description = ' '.join(word.upper() for word in description)
                outfile.write(f'{processed_title} - {processed_description}\n')