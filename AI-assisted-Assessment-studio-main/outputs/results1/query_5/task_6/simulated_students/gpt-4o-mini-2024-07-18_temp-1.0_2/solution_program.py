def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = ""
    longest_length = 0

    with open(input_filepath, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            character_name = lines[i].strip()
            i += 1
            legend_lines = []

            while i < len(lines) and lines[i].strip() != "END":
                legend_lines.append(lines[i].strip())
                i += 1

            i += 1  # skip the "END" line
            legend = ' '.join(legend_lines)
            word_count = len(legend.split())

            if word_count > longest_length:
                longest_length = word_count
                longest_character = character_name
                longest_legend = legend

    with open(output_filepath, 'w') as output_file:
        output_file.write(f'{longest_character}\n{longest_legend}')