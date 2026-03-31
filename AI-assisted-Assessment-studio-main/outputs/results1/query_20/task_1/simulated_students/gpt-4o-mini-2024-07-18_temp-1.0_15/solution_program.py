def find_winner(player1, player2):
    score1 = sum(map(int, player1.split()))
    score2 = sum(map(int, player2.split()))
    
    if score1 > score2:
        return "Player 1 Wins"
    elif score2 > score1:
        return "Player 2 Wins"
    else:
        return "Draw"