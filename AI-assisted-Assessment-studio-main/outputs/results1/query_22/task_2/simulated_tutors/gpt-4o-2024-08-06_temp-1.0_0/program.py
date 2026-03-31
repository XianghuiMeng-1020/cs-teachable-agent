def count_games_with_letter(filepath, letter):
    count = 0
    letter = letter.lower()  # Normalize the compare letter to lowercase
    with open(filepath, 'r') as file:
        for line in file:
            game_name = line.strip()  # Remove leading/trailing whitespace
            if game_name.lower().startswith(letter):  # Check if game name starts with the given letter
                count += 1
    return count

def main():
    print(count_games_with_letter('games.txt', 'C'))  # Example call

if __name__ == "__main__":
    main()