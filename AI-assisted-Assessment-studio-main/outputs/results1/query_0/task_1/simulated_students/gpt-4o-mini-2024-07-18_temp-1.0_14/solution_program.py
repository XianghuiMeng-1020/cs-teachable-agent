def play_dice_game(dice1, dice2):
    outcome = None
    sum_of_dice = dice1 + dice2

    if sum_of_dice in (7, 11):
        outcome = 'Win'
    elif sum_of_dice in (2, 3, 12):
        outcome = 'Lose'
    else:
        outcome = 'Tie'

    with open('game_log.txt', 'a') as file:
        file.write(f'{dice1}, {dice2} - {outcome}\n')