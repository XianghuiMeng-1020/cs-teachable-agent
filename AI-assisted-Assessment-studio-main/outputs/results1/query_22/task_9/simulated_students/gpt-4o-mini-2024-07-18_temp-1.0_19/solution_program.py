def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    scores = []
    for line in lines:
        name, score = line.split()
        scores.append((name, int(score)))

    for player, new_score in new_scores:
        for i in range(len(scores)):
            if scores[i][0] == player:
                if new_score > scores[i][1]:
                    scores[i] = (player, new_score)
                break
        else:
            scores.append((player, new_score))

    scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in scores:
            file.write(f'{name} {score}\n')