def find_longest_legend(input_filepath: str, output_filepath: str):
    longest_character = None
    longest_legend = ""
    
    with open(input_filepath, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            name = lines[i].strip()
            i += 1
            legend_lines = []
            while i < len(lines) and lines[i].strip() != "END":
                legend_lines.append(lines[i].strip())
                i += 1
            i += 1  # Skip over the "END" line
            legend = ' '.join(legend_lines)
            word_count = len(legend.split())
            
            if word_count > len(longest_legend.split()):
                longest_character = name
                longest_legend = legend
    
    with open(output_filepath, 'w') as output_file:
        output_file.write(f'{longest_character}\n{longest_legend}')