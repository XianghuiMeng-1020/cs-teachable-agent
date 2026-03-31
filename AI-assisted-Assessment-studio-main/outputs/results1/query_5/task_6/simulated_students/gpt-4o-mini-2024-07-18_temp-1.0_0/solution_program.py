def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = 0

    with open(input_filepath, 'r') as file:
        while True:
            character_name = file.readline().strip()
            if not character_name:
                break
            legend = ''
            while True:
                line = file.readline().strip()
                if line == 'END':
                    break
                legend += ' ' + line
            legend_word_count = len(legend.split())
            if legend_word_count > longest_legend:
                longest_legend = legend_word_count
                longest_character = (character_name, legend.strip())

    if longest_character:
        with open(output_filepath, 'w') as output_file:
            output_file.write(longest_character[0] + '\n')
            output_file.write(longest_character[1] + '\n')
