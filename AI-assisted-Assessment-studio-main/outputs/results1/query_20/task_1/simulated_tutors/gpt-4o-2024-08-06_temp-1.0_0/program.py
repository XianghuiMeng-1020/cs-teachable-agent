def find_winner(player1, player2):
    # Split the string and convert values to integers for player 1
    p1_dice = player1.split()
    p1_first_dice = int(p1_dice[0])
    p1_second_dice = int(p1_dice[1])
    # Calculate total for player 1
    player1_total = p1_first_dice + p1_second_dice

    # Split the string and convert values to integers for player 2
    p2_dice = player2.split()
    p2_first_dice = int(p2_dice[0])
    p2_second_dice = int(p2_dice[1])
    # Calculate total for player 2
    player2_total = p2_first_dice + p2_second_dice

    # Determine the winner by comparing the totals
    if player1_total > player2_total:
        return "Player 1 Wins"
    elif player2_total > player1_total:
        return "Player 2 Wins"
    else:
        return "Draw"