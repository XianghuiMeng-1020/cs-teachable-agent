def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    high_scores = []
    for line in lines:
        name, score = line.strip().split()
        high_scores.append((name, int(score)))

    for player, new_score in new_scores:
        updated = False
        for i, (name, score) in enumerate(high_scores):
            if name == player:
                if new_score > score:
                    high_scores[i] = (name, new_score)
                updated = True
                break
        if not updated:
            high_scores.append((player, new_score))

    high_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in high_scores:
            file.write(f'{name} {score}\n')