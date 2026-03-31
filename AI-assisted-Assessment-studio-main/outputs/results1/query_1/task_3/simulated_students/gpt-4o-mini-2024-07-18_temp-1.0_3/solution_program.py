def dice_game(target_score, rolls):
    total_score = sum(rolls)
    if total_score >= target_score:
        return 'WIN'
    else:
        return 'LOSE'