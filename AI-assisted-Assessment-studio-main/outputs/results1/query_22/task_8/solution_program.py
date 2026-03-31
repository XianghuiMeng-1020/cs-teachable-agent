def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        round_number = 1
        with open(filename, 'r') as check_file:
            lines = check_file.readlines()
            if lines:
                round_number = len(lines) + 1
        for scores in players_scores:
            round_data = f"Round {round_number}: " + ' '.join(map(str, scores)) + '\n'
            file.write(round_data)
            round_number += 1


def get_scores(filename):
    rounds = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            rounds.append(line.strip())
    return rounds
