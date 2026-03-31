def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            title_description = line.split('-', 1)  
            if len(title_description) == 2:
                title = title_description[0].strip()
                description = title_description[1].strip()
                reversed_title = ' '.join(reversed(title.upper().split()))
                reversed_description = ' '.join(reversed(description.upper().split()))
                outfile.write(f'{reversed_title} - {reversed_description}\n')