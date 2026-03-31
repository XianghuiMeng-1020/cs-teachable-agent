def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        words = line.split()
        word_count = {word: words.count(word) for word in set(words)}
        most_frequent_word = max(word_count, key=lambda k: (word_count[k], -words.index(k)))
        results.append(f"{most_frequent_word} {word_count[most_frequent_word]}")

    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')