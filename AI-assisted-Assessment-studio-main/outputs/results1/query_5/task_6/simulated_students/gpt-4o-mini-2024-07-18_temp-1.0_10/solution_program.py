def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = ""
    word_count = 0

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
            i += 1  # Skip the "END" line

            legend = " ".join(legend_lines)
            current_word_count = len(legend.split())

            if current_word_count > word_count:
                longest_character = character_name
                longest_legend = legend
                word_count = current_word_count

    with open(output_filepath, 'w') as outfile:
        outfile.write(f"{longest_character}\n{longest_legend}")