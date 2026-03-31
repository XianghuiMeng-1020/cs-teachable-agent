def count_games_with_letter(filepath, letter):
    count = 0
    letter = letter.lower()
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip().lower().startswith(letter):
                count += 1
    return count