def find_longest_legend(input_filepath, output_filepath):
    with open(input_filepath, 'r') as file:
        lines = file.readlines()
    
    longest_legend_name = ''
    longest_legend = ''
    current_name = ''
    current_legend = ''
    in_legend = False

    for line in lines:
        line = line.strip()
        if line == 'END':
            if len(current_legend.split()) > len(longest_legend.split()):
                longest_legend_name = current_name
                longest_legend = current_legend
            current_name = ''
            current_legend = ''
            in_legend = False
        elif not in_legend:
            current_name = line
            in_legend = True
        else:
            if current_legend:
                current_legend += ' '
            current_legend += line

    with open(output_filepath, 'w') as file:
        file.write(longest_legend_name + '\n')
        file.write(longest_legend + '\n')