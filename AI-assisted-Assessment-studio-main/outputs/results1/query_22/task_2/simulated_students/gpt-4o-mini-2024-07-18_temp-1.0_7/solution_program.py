def count_games_with_letter(filepath, letter):
    count = 0
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith(letter.upper()) or line.startswith(letter.lower()):
                count += 1
    return count