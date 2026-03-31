import os

def lucky_numbers():
    # Load player data
    if not os.path.exists('players.txt'):
        with open('results.txt', 'w') as f:
            f.write('')
        return

    with open('players.txt', 'r') as f:
        player_lines = f.readlines()

    # Load winning numbers
    if not os.path.exists('winning_numbers.txt'):
        with open('results.txt', 'w') as f:
            f.write('')
        return

    with open('winning_numbers.txt', 'r') as f:
        winning_numbers = [int(num) for num in f.readline().strip().split(",")]

    results = []

    # Find matches for each player
    for line in player_lines:
        name, number = line.strip().split(",")
        number = int(number)
        match_count = winning_numbers.count(number)
        results.append(f"{name}: {match_count}")

    # Write results to the results file
    with open('results.txt', 'w') as f:
        f.write('\n'.join(results) + '\n')