def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        stories = infile.readlines()

    with open(output_filename, 'w') as outfile:
        for story in stories:
            words = story.split()
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
            outfile.write(f'{most_frequent_word} {highest_frequency}\n')