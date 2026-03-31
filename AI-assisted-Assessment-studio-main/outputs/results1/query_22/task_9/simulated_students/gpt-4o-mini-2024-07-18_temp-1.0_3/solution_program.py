def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as f:
        lines = f.readlines()
    current_scores = []
    for line in lines:
        name, score = line.strip().split()  
        current_scores.append((name, int(score)))  

    for player, score in new_scores:
        updated = False
        for i in range(len(current_scores)):
            if current_scores[i][0] == player:
                if score > current_scores[i][1]:
                    current_scores[i] = (player, score)
                updated = True
                break
        if not updated:
            current_scores.append((player, score))

    current_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as f:
        for name, score in current_scores:
            f.write(f'{name} {score}\n')