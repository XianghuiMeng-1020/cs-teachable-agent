def find_longest_legend(input_filepath: str, output_filepath: str):
    # Read the input file and process characters and legends
    with open(input_filepath, 'r') as file:
        lines = file.readlines()

    longest_legend_length = 0
    longest_character = ''
    longest_legend = ''

    i = 0
    while i < len(lines):
        character_name = lines[i].strip()
        legend = []

        # Read the legend until 'END' is found
        i += 1
        while i < len(lines) and lines[i].strip() != 'END':
            legend.append(lines[i].strip())
            i += 1

        # Calculate the word count of the legend
        legend_content = ' '.join(legend)
        word_count = len(legend_content.split())

        # If the legend is the longest so far, store it
        if word_count > longest_legend_length:
            longest_legend_length = word_count
            longest_character = character_name
            longest_legend = legend_content

        # Move to the next character (next line after END)
        i += 1

    # Write the longest legend to the output file
    with open(output_filepath, 'w') as file:
        file.write(f"{longest_character}\n{longest_legend}\n")