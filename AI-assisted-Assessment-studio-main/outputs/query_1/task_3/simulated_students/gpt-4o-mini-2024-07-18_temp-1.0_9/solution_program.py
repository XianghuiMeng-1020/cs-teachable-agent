def calculate_awards(warrior_achievements):
    award_titles = []
    for achievements in warrior_achievements:
        if achievements == 0:
            award_titles.append('Novice')
        elif 1 <= achievements <= 5:
            award_titles.append('Adept')
        elif 6 <= achievements <= 10:
            award_titles.append('Veteran')
        elif achievements > 10:
            award_titles.append('Elite')
    return award_titles