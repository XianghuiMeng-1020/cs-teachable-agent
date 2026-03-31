def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        lines = file.readlines()
    current_records = []
    for line in lines:
        name, score = line.split()
        current_records.append((name, int(score)))
    
    for new_name, new_score in new_scores:
        found = False
        for i, (name, score) in enumerate(current_records):
            if name == new_name:
                if new_score > score:
                    current_records[i] = (name, new_score)
                found = True
                break
        if not found:
            current_records.append((new_name, new_score))

    current_records.sort(key=lambda x: x[1], reverse=True)
    
    with open(records_file, 'w') as file:
        for name, score in current_records:
            file.write(f"{name} {score}\n")