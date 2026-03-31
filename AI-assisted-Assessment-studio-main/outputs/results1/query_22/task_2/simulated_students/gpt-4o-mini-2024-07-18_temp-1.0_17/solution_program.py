def count_games_with_letter(filepath, letter):
    with open(filepath, 'r') as file:
        games = file.readlines()
    count = 0
    letter = letter.lower()
    for game in games:
        if game.strip().lower().startswith(letter):
            count += 1
    return count