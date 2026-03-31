def calculate_awards(warrior_achievements):
    awards = []
    for wins in warrior_achievements:
        if wins == 0:
            awards.append('Novice')
        elif 1 <= wins <= 5:
            awards.append('Adept')
        elif 6 <= wins <= 10:
            awards.append('Veteran')
        elif wins > 10:
            awards.append('Elite')
    return awards