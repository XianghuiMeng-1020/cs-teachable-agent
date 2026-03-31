def find_winner(player1, player2):
    # Split the strings to get individual dice rolls
    p1_rolls = list(map(int, player1.split()))
    p2_rolls = list(map(int, player2.split()))
    
    # Calculate the total score for each player
    p1_score = sum(p1_rolls)
    p2_score = sum(p2_rolls)
    
    # Determine the winner
    if p1_score > p2_score:
        return "Player 1 Wins"
    elif p2_score > p1_score:
        return "Player 2 Wins"
    else:
        return "Draw"