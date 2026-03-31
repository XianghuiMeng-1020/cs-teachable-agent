def play_dice_game(dice1, dice2):
    outcome = ""
    dice_sum = dice1 + dice2
    if dice_sum == 7 or dice_sum == 11:
        outcome = "Win"
    elif dice_sum in (2, 3, 12):
        outcome = "Lose"
    else:
        outcome = "Tie"
    result = f"{dice1}, {dice2} - {outcome}\n"
    with open('game_log.txt', 'a') as file:
        file.write(result)