def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0
    longest_legend_text = ""

    with open(input_filepath, 'r') as file:
        current_character = None
        current_legend = []

        for line in file:
            line = line.strip()
            if line == "END":
                if current_character:
                    word_count = len(' '.join(current_legend).split())
                    if word_count > longest_legend:
                        longest_legend = word_count
                        longest_character = current_character
                        longest_legend_text = ' '.join(current_legend)
                # Reset for the next character
                current_character = None
                current_legend = []
            elif current_character is None:
                current_character = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as output_file:
        if longest_character:
            output_file.write(longest_character + '\n' + longest_legend_text)
