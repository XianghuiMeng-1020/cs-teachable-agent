def find_winner(score_a, score_b):
    if score_a > score_b:
        return "Player A wins"
    elif score_b > score_a:
        return "Player B wins"
    else:
        return "Tie"