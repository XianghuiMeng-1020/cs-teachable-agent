def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_name = None
    longest_legend = ''
    current_name = None
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                if len(current_legend) > len(longest_legend.split()):
                    longest_legend = ' '.join(current_legend)
                    longest_name = current_name
                # Reset current legend
                current_name = None
                current_legend = []
            elif current_name is None:
                current_name = line
            else:
                current_legend.append(line)

    if longest_name and longest_legend:
        with open(output_filepath, 'w') as output_file:
            output_file.write(f"{longest_name}\n{longest_legend}")