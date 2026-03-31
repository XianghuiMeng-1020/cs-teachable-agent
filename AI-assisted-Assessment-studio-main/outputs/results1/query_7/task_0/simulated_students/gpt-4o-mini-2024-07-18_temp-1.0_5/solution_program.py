def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            words = line.strip().split()
            word_count = {}
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            most_frequent_word = None
            max_frequency = 0
            for word in words:
                if word_count[word] > max_frequency:
                    most_frequent_word = word
                    max_frequency = word_count[word]
            outfile.write(f'{most_frequent_word} {max_frequency}\n')