def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    scores = []
    for line in lines:
        name, score = line.strip().rsplit(' ', 1)
        score = int(score)
        scores.append((name, score))

    for player, new_score in new_scores:
        for i, (name, score) in enumerate(scores):
            if name == player:
                if new_score > score:
                    scores[i] = (name, new_score)
                break
        else:
            scores.append((player, new_score))

    scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in scores:
            file.write(f'{name} {score}\n')