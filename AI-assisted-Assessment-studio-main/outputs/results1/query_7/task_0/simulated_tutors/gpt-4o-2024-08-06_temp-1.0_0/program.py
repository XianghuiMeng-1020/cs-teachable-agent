def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if line.strip() == "":
                outfile.write("\n")
                continue
            words = line.split()
            word_count = {}
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            # Find the word with the highest frequency
            most_frequent_word = max(word_count, key=lambda word: (word_count[word], -words.index(word)))
            frequency = word_count[most_frequent_word]
            outfile.write(f"{most_frequent_word} {frequency}\n")