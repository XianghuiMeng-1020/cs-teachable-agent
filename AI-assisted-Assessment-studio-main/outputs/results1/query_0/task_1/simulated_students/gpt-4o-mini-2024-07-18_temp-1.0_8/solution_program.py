def play_dice_game(dice1, dice2):
    # Calculate the sum of the dice rolls
    total = dice1 + dice2
    
    # Determine the outcome
    if total in [7, 11]:
        outcome = 'Win'
    elif total in [2, 3, 12]:
        outcome = 'Lose'
    else:
        outcome = 'Tie'
    
    # Log the result to 'game_log.txt'
    with open('game_log.txt', 'a') as file:
        file.write(f'{dice1}, {dice2} - {outcome}\n')