def board_game_feedback(score):
    if score >= 90:
        return "You're a board game master!"
    elif score >= 75:
        return "Great job! You're on the way to mastery."
    elif score >= 50:
        return "Good effort. Keep practicing!"
    elif score >= 25:
        return "Not bad, but there's room for improvement."
    else:
        return "Needs more practice to improve."