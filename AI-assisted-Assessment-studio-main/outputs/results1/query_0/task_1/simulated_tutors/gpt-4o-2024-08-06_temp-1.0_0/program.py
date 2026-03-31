def play_dice_game(dice1, dice2):
    """
    Simulates a game of chance using two dice rolls and logs the outcome.
    The outcome ('Win', 'Lose', or 'Tie') is determined based on the sum of dice rolls
    and is then written to 'game_log.txt'.
    """
    # Calculate the sum of the dice
    dice_sum = dice1 + dice2

    # Determine the outcome based on the sum of the dice
    if dice_sum in [7, 11]:
        outcome = 'Win'
    elif dice_sum in [2, 3, 12]:
        outcome = 'Lose'
    else:
        outcome = 'Tie'

    # Create the log entry
    log_entry = f"{dice1}, {dice2} - {outcome}"

    # Write the log entry to the file
    with open('game_log.txt', 'a') as file:
        file.write(log_entry + '\n')