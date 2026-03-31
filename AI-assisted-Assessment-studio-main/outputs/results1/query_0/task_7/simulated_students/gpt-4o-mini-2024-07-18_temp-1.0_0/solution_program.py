def game_of_chance(filename):
    score = 10
    bet = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                # It's a bet amount
                bet = int(line) if int(line) <= score else 0
            elif line == 'win':
                score += bet
            elif line == 'lose':
                score -= bet
            elif line == 'draw':
                pass
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))