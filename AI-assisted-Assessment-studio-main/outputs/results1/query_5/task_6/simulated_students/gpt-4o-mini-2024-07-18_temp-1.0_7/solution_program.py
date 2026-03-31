def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0
    current_character = None
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == 'END':
                # Count words in the current legend
                word_count = sum(len(legend.split()) for legend in current_legend)
                if word_count > longest_legend:
                    longest_legend = word_count
                    longest_character = current_character
                current_character = None
                current_legend = []
            elif current_character is None:
                # First line must be character's name
                current_character = line
            else:
                # Append lines to the current legend
                current_legend.append(line)

    if longest_character:
        with open(output_filepath, 'w') as output_file:
            output_file.write(f'{longest_character}\n')
            output_file.write('\n'.join(current_legend))
