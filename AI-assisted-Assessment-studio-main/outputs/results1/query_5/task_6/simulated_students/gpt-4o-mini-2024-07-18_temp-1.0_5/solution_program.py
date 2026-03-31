def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_legend = ""
    longest_character = ""
    current_character = ""
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                # Calculate the number of words in the current legend
                word_count = len(' '.join(current_legend).split())
                # Update the longest legend if this one is longer
                if word_count > len(longest_legend.split()):
                    longest_legend = ' '.join(current_legend)
                    longest_character = current_character
                # Reset for the next character
                current_character = ""
                current_legend = []
            elif current_character == "":
                current_character = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as output_file:
        output_file.write(f"{longest_character}\n{longest_legend}")