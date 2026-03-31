def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()

    current_scores = []
    for line in lines:
        name, score = line.strip().split()
        current_scores.append((name, int(score)))

    for new_name, new_score in new_scores:
        updated = False
        for i, (name, score) in enumerate(current_scores):
            if name == new_name:
                if new_score > score:
                    current_scores[i] = (name, new_score)
                updated = True
                break
        if not updated:
            current_scores.append((new_name, new_score))

    current_scores.sort(key=lambda x: x[1], reverse=True)

    with open(records_file, 'w') as file:
        for name, score in current_scores:
            file.write(f'{name} {score}\n')