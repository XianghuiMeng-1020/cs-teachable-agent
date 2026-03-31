def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0

    with open(input_filepath, 'r') as file:
        while True:
            # Read character name
            character_name = file.readline().strip()
            if not character_name:
                break
            # Read legend
            legend_lines = []
            while True:
                line = file.readline().strip()
                if line == "END":
                    break
                legend_lines.append(line)
            legend = " ".join(legend_lines)
            # Count words in legend
            word_count = len(legend.split())
            # Determine if this legend is the longest
            if word_count > longest_legend:
                longest_legend = word_count
                longest_character = (character_name, legend)

    # Write the result to output file
    if longest_character:
        with open(output_filepath, 'w') as outfile:
            outfile.write(longest_character[0] + '\n')
            outfile.write(longest_character[1] + '\n')