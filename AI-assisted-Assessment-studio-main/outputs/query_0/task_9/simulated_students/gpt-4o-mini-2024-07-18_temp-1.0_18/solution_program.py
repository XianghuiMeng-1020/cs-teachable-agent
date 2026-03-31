import random

def coin_flip_game(rounds):
    heads_count = 0
    tails_count = 0
    with open('flips_log.txt', 'w') as log:
        for _ in range(rounds):
            flip = 'Heads' if random.randint(0, 1) == 0 else 'Tails'
            log.write(flip + '\n')
            if flip == 'Heads':
                heads_count += 1
            else:
                tails_count += 1
    if heads_count > tails_count:
        return 'Heads'
    elif tails_count > heads_count:
        return 'Tails'
    else:
        return 'Draw'