import random

def coin_flip_game(rounds):
    heads_count = 0
    tails_count = 0
    flips_log = []

    for _ in range(rounds):
        flip = 'Heads' if random.randint(0, 1) == 0 else 'Tails'
        flips_log.append(flip)
        if flip == 'Heads':
            heads_count += 1
        else:
            tails_count += 1

    with open('flips_log.txt', 'w') as f:
        for result in flips_log:
            f.write(result + '\n')

    if heads_count > tails_count:
        return 'Heads'
    elif tails_count > heads_count:
        return 'Tails'
    else:
        return 'Draw'