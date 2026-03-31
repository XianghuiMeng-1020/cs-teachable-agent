def dice_game(target_score, rolls):
    total_score = sum(rolls)
    return 'WIN' if total_score >= target_score else 'LOSE'