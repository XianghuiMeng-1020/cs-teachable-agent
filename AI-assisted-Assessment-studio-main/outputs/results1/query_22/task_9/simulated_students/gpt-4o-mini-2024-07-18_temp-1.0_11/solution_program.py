def manage_high_scores(records_file, new_scores):
    # Read the current high scores from the file
    with open(records_file, 'r') as file:
        lines = file.readlines()

    # Create a list to hold the current high scores
    current_scores = []
    for line in lines:
        name, score = line.strip().rsplit(' ', 1)
        current_scores.append((name, int(score)))

    # Update the scores with new_scores
    for new_name, new_score in new_scores:
        updated = False
        for index, (name, score) in enumerate(current_scores):
            if name == new_name:
                if new_score > score:
                    current_scores[index] = (name, new_score)
                updated = True
                break
        if not updated:
            current_scores.append((new_name, new_score))

    # Sort the scores in descending order
    current_scores.sort(key=lambda x: x[1], reverse=True)

    # Write the updated scores back to the file
    with open(records_file, 'w') as file:
        for name, score in current_scores:
            file.write(f'{name} {score}\n')