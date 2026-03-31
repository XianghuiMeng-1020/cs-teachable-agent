def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()
    high_scores = []
    for line in lines:
        parts = line.strip().split(' ')
        name = parts[0]
        score = int(parts[1])
        high_scores.append((name, score))

    for player, new_score in new_scores:
        found = False
        for i in range(len(high_scores)):
            if high_scores[i][0] == player:
                if new_score > high_scores[i][1]:
                    high_scores[i] = (player, new_score)
                found = True
                break
        if not found:
            high_scores.append((player, new_score))

    high_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in high_scores:
            file.write(f'{name} {score}\n')
