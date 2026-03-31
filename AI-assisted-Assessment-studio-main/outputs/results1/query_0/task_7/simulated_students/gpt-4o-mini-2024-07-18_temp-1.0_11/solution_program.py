def game_of_chance(filename):
    score = 10
    bet_amount = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                bet_amount = int(line)
                if bet_amount > score:
                    bet_amount = 0  # Ignore bet if it's more than current score
            elif line == 'win':
                score += bet_amount
            elif line == 'lose':
                score -= bet_amount
            elif line == 'draw':
                pass  # score remains unchanged
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))