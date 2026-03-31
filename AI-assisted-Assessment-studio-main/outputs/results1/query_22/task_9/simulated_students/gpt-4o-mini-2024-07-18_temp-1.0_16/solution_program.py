def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    high_scores = []
    for line in lines:
        player, score = line.rsplit(' ', 1)
        score = int(score.strip())
        high_scores.append((player, score))

    for player, new_score in new_scores:
        found = False
        for i in range(len(high_scores)):
            if high_scores[i][0] == player:
                found = True
                if new_score > high_scores[i][1]:
                    high_scores[i] = (player, new_score)
                break
        if not found:
            high_scores.append((player, new_score))

    high_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for player, score in high_scores:
            file.write(f'{player} {score}\n')