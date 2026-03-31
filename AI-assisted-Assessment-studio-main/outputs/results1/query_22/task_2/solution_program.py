def count_games_with_letter(filepath, letter):
    count = 0
    letter = letter.lower()
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for game in lines:
            if game[0].lower() == letter:
                count += 1
    return count