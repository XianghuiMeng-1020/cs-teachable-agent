def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    current_scores = []
    for line in lines:
        name, score = line.strip().split()
        current_scores.append((name, int(score)))

    for new_name, new_score in new_scores:
        for i in range(len(current_scores)):
            if current_scores[i][0] == new_name:
                if new_score > current_scores[i][1]:
                    current_scores[i] = (new_name, new_score)
                break
        else:
            current_scores.append((new_name, new_score))

    current_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in current_scores:
            file.write(f'{name} {score}\n')