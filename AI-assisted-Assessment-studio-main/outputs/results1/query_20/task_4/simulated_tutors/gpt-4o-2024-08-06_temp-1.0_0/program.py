def board_game_feedback(score):
    if score >= 90:
        return "You're a board game master!"
    elif 75 <= score <= 89:
        return "Great job! You're on the way to mastery."
    elif 50 <= score <= 74:
        return "Good effort. Keep practicing!"
    elif 25 <= score <= 49:
        return "Not bad, but there's room for improvement."
    else:
        return "Needs more practice to improve."