def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        words = line.strip().split()
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        most_frequent_word = None
        highest_frequency = 0
        for word in words:
            if word_count[word] > highest_frequency:
                most_frequent_word = word
                highest_frequency = word_count[word]
        results.append(f"{most_frequent_word} {highest_frequency}")

    with open(output_filename, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')