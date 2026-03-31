def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    high_scores = []
    for line in lines:
        name, score = line.strip().split()
        high_scores.append((name, int(score)))

    for new_score in new_scores:
        name, score = new_score
        for i in range(len(high_scores)):
            if high_scores[i][0] == name:
                if score > high_scores[i][1]:
                    high_scores[i] = (name, score)
                break
        else:
            high_scores.append((name, score))

    high_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in high_scores:
            file.write(f'{name} {score}\n')