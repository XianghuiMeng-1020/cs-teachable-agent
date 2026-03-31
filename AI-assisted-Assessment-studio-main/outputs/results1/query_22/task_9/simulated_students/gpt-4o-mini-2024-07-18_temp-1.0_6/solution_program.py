def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    existing_scores = []
    for line in lines:
        name, score = line.strip().split()  
        existing_scores.append((name, int(score)))

    for player, new_score in new_scores:
        for i in range(len(existing_scores)):
            if existing_scores[i][0] == player:
                if new_score > existing_scores[i][1]:
                    existing_scores[i] = (player, new_score)
                break
        else:
            existing_scores.append((player, new_score))

    existing_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in existing_scores:
            file.write(f'{name} {score}\n')