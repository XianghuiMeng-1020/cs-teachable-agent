def classify_hero(traits):
    hero_category = 'Unsung Hero'
    if traits['strength'] > 50 and traits['strength'] >= traits['wisdom'] and traits['strength'] >= traits['courage']:
        hero_category = 'Warrior'
    elif traits['wisdom'] > 50 and traits['wisdom'] >= traits['strength'] and traits['wisdom'] >= traits['courage']:
        hero_category = 'Seer'
    elif traits['courage'] > 50 and traits['courage'] >= traits['strength'] and traits['courage'] >= traits['wisdom']:
        hero_category = 'Champion'
    return hero_category