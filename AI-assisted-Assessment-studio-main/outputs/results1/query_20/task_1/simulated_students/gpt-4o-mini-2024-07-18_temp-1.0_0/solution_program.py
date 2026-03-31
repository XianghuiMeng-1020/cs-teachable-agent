def find_winner(player1, player2):
    p1_dice = list(map(int, player1.split()))
    p2_dice = list(map(int, player2.split()))
    total1 = sum(p1_dice)
    total2 = sum(p2_dice)
    if total1 > total2:
        return "Player 1 Wins"
    elif total2 > total1:
        return "Player 2 Wins"
    else:
        return "Draw"