def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0

    with open(input_filepath, 'r') as file:
        character = None
        legend = []
        for line in file:
            line = line.strip()
            if line == "END":
                if character is not None:
                    word_count = len(' '.join(legend).split())
                    if word_count > longest_legend:
                        longest_legend = word_count
                        longest_character = character
                character = None
                legend = []
            elif character is None:
                character = line
            else:
                legend.append(line)

    if longest_character is not None:
        with open(output_filepath, 'w') as output_file:
            output_file.write(f'{longest_character}\n')
            output_file.write(' '.join(legend))