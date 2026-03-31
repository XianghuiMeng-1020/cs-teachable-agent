def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        stories = infile.readlines()

    with open(output_filename, 'w') as outfile:
        for story in stories:
            words = story.split()
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
                    most_frequent_word = word
                    max_frequency = frequency[word]

            outfile.write(f'{most_frequent_word} {max_frequency}\n')