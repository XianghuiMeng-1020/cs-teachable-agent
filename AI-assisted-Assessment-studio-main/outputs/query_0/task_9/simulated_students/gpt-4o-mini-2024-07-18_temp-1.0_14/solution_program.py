import random

def coin_flip_game(rounds):
    heads_count = 0
    tails_count = 0
    with open('flips_log.txt', 'w') as log_file:
        for _ in range(rounds):
            flip_result = 'Heads' if random.choice([True, False]) else 'Tails'
            log_file.write(flip_result + '\n')
            if flip_result == 'Heads':
                heads_count += 1
            else:
                tails_count += 1
    if heads_count > tails_count:
        return 'Heads'
    elif tails_count > heads_count:
        return 'Tails'
    else:
        return 'Draw'