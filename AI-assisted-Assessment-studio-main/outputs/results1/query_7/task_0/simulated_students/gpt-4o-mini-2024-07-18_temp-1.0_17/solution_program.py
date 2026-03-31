def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    results = []
    for line in lines:
        words = line.split()
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
                max_frequency = word_count[word]
                most_frequent_word = word
        results.append(f'{most_frequent_word} {max_frequency}')
    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')