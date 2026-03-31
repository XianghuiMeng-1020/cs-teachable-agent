def dice_game(target_score, rolls):
    current_score = 0
    for roll in rolls:
        current_score += roll
        if current_score >= target_score:
            return 'WIN'
    return 'LOSE'