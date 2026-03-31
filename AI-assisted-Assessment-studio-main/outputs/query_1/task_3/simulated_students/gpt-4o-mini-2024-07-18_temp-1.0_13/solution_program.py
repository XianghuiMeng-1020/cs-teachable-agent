def calculate_awards(warrior_achievements):
    awards = []
    for accomplishments in warrior_achievements:
        if accomplishments == 0:
            awards.append('Novice')
        elif 1 <= accomplishments <= 5:
            awards.append('Adept')
        elif 6 <= accomplishments <= 10:
            awards.append('Veteran')
        else:
            awards.append('Elite')
    return awards