def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0

    with open(input_filepath, 'r') as file:
        character_name = None
        legend_lines = []

        for line in file:
            line = line.strip()
            if line == 'END':
                if character_name:
                    # Count words in the legend
                    current_legend = ' '.join(legend_lines)
                    word_count = len(current_legend.split())

                    # Check if this legend is the longest
                    if word_count > longest_legend:
                        longest_legend = word_count
                        longest_character = (character_name, current_legend)

                # Reset for the next character
                character_name = None
                legend_lines = []
            elif character_name is None:
                # First line after the last END is the character name
                character_name = line
            else:
                # Collecting legend lines
                legend_lines.append(line)

    if longest_character:
        # Writing the result to output file
        with open(output_filepath, 'w') as output_file:
            output_file.write(longest_character[0] + '\n' + longest_character[1])