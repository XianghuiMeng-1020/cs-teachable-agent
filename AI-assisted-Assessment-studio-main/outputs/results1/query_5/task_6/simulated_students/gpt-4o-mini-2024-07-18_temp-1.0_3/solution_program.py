def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend_length = 0
    longest_legend = ""

    with open(input_filepath, 'r') as infile:
        lines = infile.readlines()
        i = 0
        while i < len(lines):
            character_name = lines[i].strip()
            i += 1
            legend = ""

            while i < len(lines) and lines[i].strip() != "END":
                legend += lines[i].strip() + " "
                i += 1

            # Skip the 'END' line
            if i < len(lines) and lines[i].strip() == "END":
                i += 1

            # Calculate the number of words in the legend
            word_count = len(legend.split())

            if word_count > longest_legend_length:
                longest_legend_length = word_count
                longest_character = character_name
                longest_legend = legend.strip()

    with open(output_filepath, 'w') as outfile:
        outfile.write(f'{longest_character}\n{longest_legend}')