def calculate_awards(warrior_achievements):
    titles = []
    for achievements in warrior_achievements:
        if achievements == 0:
            titles.append('Novice')
        elif 1 <= achievements <= 5:
            titles.append('Adept')
        elif 6 <= achievements <= 10:
            titles.append('Veteran')
        elif achievements > 10:
            titles.append('Elite')
    return titles