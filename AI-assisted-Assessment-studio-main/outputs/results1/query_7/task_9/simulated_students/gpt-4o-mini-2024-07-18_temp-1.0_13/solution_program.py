def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if '-' in line:
                title, description = line.split('-', 1)
                title = title.strip()
                description = description.strip()
                
                # Reverse the words and convert to uppercase
                reversed_title = ' '.join(title.split()[::-1]).upper()
                reversed_description = ' '.join(description.split()[::-1]).upper()
                
                # Write to output file
                outfile.write(f'{reversed_title} - {reversed_description}\n')