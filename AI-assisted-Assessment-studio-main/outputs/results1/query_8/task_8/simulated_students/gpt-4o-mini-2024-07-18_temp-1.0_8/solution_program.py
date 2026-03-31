def classify_hero(traits):
    if traits['strength'] > traits['wisdom'] and traits['strength'] > traits['courage'] and traits['strength'] > 50:
        return 'Warrior'
    elif traits['wisdom'] > traits['strength'] and traits['wisdom'] > traits['courage'] and traits['wisdom'] > 50:
        return 'Seer'
    elif traits['courage'] > traits['strength'] and traits['courage'] > traits['wisdom'] and traits['courage'] > 50:
        return 'Champion'
    return 'Unsung Hero'