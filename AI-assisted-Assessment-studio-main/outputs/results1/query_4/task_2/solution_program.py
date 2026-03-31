def play_dice_game(target):
    current_score = 0
    rolls = 0
    die_max = 6  # Max value of a single die roll
    while current_score < target:
        rolls += 1
        if current_score + die_max >= target:
            current_score = target
        else:
            current_score += die_max
    return rolls