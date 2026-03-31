def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_name = None
    longest_legend = ""
    current_name = None
    current_legend = []

    with open(input_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END":
                if current_name:
                    word_count = len(" ".join(current_legend).split())
                    if word_count > len(longest_legend.split()):
                        longest_name = current_name
                        longest_legend = " ".join(current_legend)
                # Reset current legend
                current_name = None
                current_legend = []
            elif current_name is None:
                current_name = line
            else:
                current_legend.append(line)

    with open(output_filepath, 'w') as output_file:
        output_file.write(longest_name + "\n")
        output_file.write(longest_legend)