def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()
    scores = [line.strip().split() for line in lines]
    scores = [(name, int(score)) for name, score in scores]
    for player, new_score in new_scores:
        updated = False
        for i in range(len(scores)):
            if scores[i][0] == player:
                if new_score > scores[i][1]:
                    scores[i] = (player, new_score)
                updated = True
                break
        if not updated:
            scores.append((player, new_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    with open(records_file, 'w') as file:
        for player, score in scores:
            file.write(f'{player} {score}\n')