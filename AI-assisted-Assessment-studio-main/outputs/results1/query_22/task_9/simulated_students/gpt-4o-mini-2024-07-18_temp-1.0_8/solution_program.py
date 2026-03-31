def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    scores = []
    for line in lines:
        name, score = line.strip().rsplit(' ', 1)
        scores.append((name, int(score)))

    for new_name, new_score in new_scores:
        for i in range(len(scores)):
            name, score = scores[i]
            if name == new_name:
                if new_score > score:
                    scores[i] = (name, new_score)
                break
        else:
            scores.append((new_name, new_score))

    scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in scores:
            file.write(f'{name} {score}\n')