def find_winner(player1, player2):
    p1_rolls = player1.split()
    p2_rolls = player2.split()
    
    p1_score = int(p1_rolls[0]) + int(p1_rolls[1])
    p2_score = int(p2_rolls[0]) + int(p2_rolls[1])
    
    if p1_score > p2_score:
        return "Player 1 Wins"
    elif p2_score > p1_score:
        return "Player 2 Wins"
    else:
        return "Draw"