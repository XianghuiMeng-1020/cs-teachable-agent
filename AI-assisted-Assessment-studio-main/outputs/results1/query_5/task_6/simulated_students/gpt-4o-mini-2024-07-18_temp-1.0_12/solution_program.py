def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_legend = ""
    longest_character = ""
    current_character = None
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                if current_character and len(current_legend) > len(longest_legend.split()):
                    longest_legend = ' '.join(current_legend)
                    longest_character = current_character
                current_character = None
                current_legend = []
            elif current_character is None:
                current_character = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as outfile:
        outfile.write(f'{longest_character}\n{longest_legend}')