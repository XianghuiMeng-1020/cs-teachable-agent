def manage_high_scores(records_file, new_scores):
    with open(records_file, 'r') as file:
        records = [line.strip().split() for line in file.readlines()]

    for name, score in new_scores:
        score = int(score)
        for record in records:
            if record[0] == name:
                if int(record[1]) < score:
                    record[1] = str(score)
                break
        else:
            records.append([name, str(score)])

    records.sort(key=lambda x: int(x[1]), reverse=True)

    with open(records_file, 'w') as file:
        for record in records:
            file.write(f'{record[0]} {record[1]}\n')