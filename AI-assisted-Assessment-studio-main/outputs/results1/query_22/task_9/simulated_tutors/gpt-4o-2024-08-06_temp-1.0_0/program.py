def manage_high_scores(records_file, new_scores):
    # Read the existing scores from the file
    with open(records_file, 'r') as file:
        lines = file.readlines()
        scores = [line.strip().split() for line in lines]
        scores = [(name, int(score)) for name, score in scores]

    # Update scores with new entries
    for name, new_score in new_scores:
        updated = False
        for i, (existing_name, existing_score) in enumerate(scores):
            if existing_name == name:
                if new_score > existing_score:
                    scores[i] = (name, new_score)
                updated = True
                break
        if not updated:
            scores.append((name, new_score))

    # Sort the scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Write the updated scores back to the file
    with open(records_file, 'w') as file:
        for name, score in scores:
            file.write(f"{name} {score}\n")