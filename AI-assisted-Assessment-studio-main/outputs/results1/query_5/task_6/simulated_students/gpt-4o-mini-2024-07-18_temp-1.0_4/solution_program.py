def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0

    with open(input_filepath, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            character = lines[i].strip()
            i += 1
            legend = ''
            while i < len(lines) and lines[i].strip() != 'END':
                legend += lines[i].strip() + ' '
                i += 1
            if i < len(lines) and lines[i].strip() == 'END':
                i += 1
            legend_word_count = len(legend.split())
            if legend_word_count > longest_legend:
                longest_legend = legend_word_count
                longest_character = (character, legend.strip())

    if longest_character:
        with open(output_filepath, 'w') as output_file:
            output_file.write(longest_character[0] + '\n')
            output_file.write(longest_character[1])
