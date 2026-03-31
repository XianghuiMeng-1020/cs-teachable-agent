def count_games_with_letter(filepath, letter):
    count = 0
    letter = letter.lower()
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and line[0].lower() == letter:
                count += 1
    return count