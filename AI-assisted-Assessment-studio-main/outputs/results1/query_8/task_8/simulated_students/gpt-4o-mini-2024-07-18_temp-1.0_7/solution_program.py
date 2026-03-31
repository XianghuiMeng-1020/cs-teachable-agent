def classify_hero(traits):
    if traits['strength'] > 50 and (traits['strength'] >= traits['wisdom']) and (traits['strength'] >= traits['courage']):
        return 'Warrior'
    elif traits['wisdom'] > 50 and (traits['wisdom'] >= traits['strength']) and (traits['wisdom'] >= traits['courage']):
        return 'Seer'
    elif traits['courage'] > 50 and (traits['courage'] >= traits['strength']) and (traits['courage'] >= traits['wisdom']):
        return 'Champion'
    else:
        return 'Unsung Hero'