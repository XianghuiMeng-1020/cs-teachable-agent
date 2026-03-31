def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            words = line.split()
            frequency = {}  
            for word in words:
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 1
            most_frequent_word = None
            max_frequency = 0
            for word in words:
                if frequency[word] > max_frequency:
                    max_frequency = frequency[word]
                    most_frequent_word = word
            outfile.write(f'{most_frequent_word} {max_frequency}\n')