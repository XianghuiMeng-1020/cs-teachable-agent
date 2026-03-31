def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0
    current_character = None
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == 'END':
                if current_character and len(current_legend) > longest_legend:
                    longest_character = current_character
                    longest_legend = len(current_legend)
                current_character = None
                current_legend = []
            elif current_character is None:
                current_character = line
            else:
                current_legend.append(line)

    if longest_character:
        with open(output_filepath, 'w') as output_file:
            output_file.write(longest_character + '\n')
            output_file.write('\n'.join(current_legend))