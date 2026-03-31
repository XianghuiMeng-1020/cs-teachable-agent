def find_winner(player1, player2):
    p1_dice = list(map(int, player1.split()))
    p2_dice = list(map(int, player2.split()))
    p1_score = sum(p1_dice)
    p2_score = sum(p2_dice)
    if p1_score > p2_score:
        return "Player 1 Wins"
    elif p2_score > p1_score:
        return "Player 2 Wins"
    else:
        return "Draw"