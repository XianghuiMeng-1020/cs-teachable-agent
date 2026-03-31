def calculate_awards(warrior_achievements):
    awards = []
    for achievements in warrior_achievements:
        if achievements == 0:
            awards.append('Novice')
        elif 1 <= achievements <= 5:
            awards.append('Adept')
        elif 6 <= achievements <= 10:
            awards.append('Veteran')
        elif achievements > 10:
            awards.append('Elite')
    return awards