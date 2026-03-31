def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_legend = ""
    character_name = ""
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                if len(current_legend) > len(longest_legend.split()):
                    longest_legend = ' '.join(current_legend)
                    character_name = current_character
                current_legend = []
            elif current_legend == []:
                current_character = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as file:
        file.write(character_name + '\n' + longest_legend)