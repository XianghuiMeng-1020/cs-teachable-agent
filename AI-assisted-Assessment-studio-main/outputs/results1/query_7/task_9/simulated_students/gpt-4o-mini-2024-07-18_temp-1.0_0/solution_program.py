def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    processed_lines = []
    for line in lines:
        line = line.strip()
        if ' - ' in line:
            title, description = line.split(' - ', 1)
            title = ' '.join(reversed(title.strip().split())).upper()
            description = ' '.join(reversed(description.strip().split())).upper()
            processed_lines.append(f'{title} - {description}') 

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(processed_lines) + '\n')