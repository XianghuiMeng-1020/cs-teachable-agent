def find_winner(player1, player2):
    p1_score = sum(map(int, player1.split()))
    p2_score = sum(map(int, player2.split()))
    if p1_score > p2_score:
        return "Player 1 Wins"
    elif p2_score > p1_score:
        return "Player 2 Wins"
    else:
        return "Draw"