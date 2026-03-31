def calculate_awards(warrior_achievements):
    titles = []
    for wins in warrior_achievements:
        if wins == 0:
            titles.append('Novice')
        elif 1 <= wins <= 5:
            titles.append('Adept')
        elif 6 <= wins <= 10:
            titles.append('Veteran')
        elif wins > 10:
            titles.append('Elite')
    return titles