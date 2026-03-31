def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_legend = ""
    longest_character = ""
    current_character = ""
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                # Finished reading a legend
                legend_text = ' '.join(current_legend)
                if len(legend_text.split()) > len(longest_legend.split()):
                    longest_legend = legend_text
                    longest_character = current_character
                # Reset for the next character
                current_character = ""
                current_legend = []
            elif current_character == "":
                # New character name
                current_character = line
            else:
                # In legend content
                current_legend.append(line)

    with open(output_filepath, 'w') as output_file:
        output_file.write(longest_character + '\n')
        output_file.write(longest_legend)