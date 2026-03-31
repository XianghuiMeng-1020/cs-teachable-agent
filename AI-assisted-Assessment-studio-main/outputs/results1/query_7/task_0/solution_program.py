def analyze_myths(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    results = []
    for line in lines:
        words = line.strip().split()
        if not words:
            results.append('')
            continue
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        most_frequent = max(word_count.values())
        for word in words:
            if word_count[word] == most_frequent:
                results.append(f'{word} {most_frequent}')
                break
    with open(output_filename, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')
