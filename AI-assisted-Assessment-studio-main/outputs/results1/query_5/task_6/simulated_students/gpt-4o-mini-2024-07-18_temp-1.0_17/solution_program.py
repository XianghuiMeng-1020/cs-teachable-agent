def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = ""
    longest_word_count = 0
    current_character = None
    current_legend = []

    with open(input_filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line == "END":
                if current_character is not None:
                    word_count = len(' '.join(current_legend).split())
                    if word_count > longest_word_count:
                        longest_word_count = word_count
                        longest_character = current_character
                        longest_legend = ' '.join(current_legend)
                # Reset for the next character
                current_character = None
                current_legend = []
            elif current_character is None:
                current_character = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as outfile:
        outfile.write(f'{longest_character}\n{longest_legend}')