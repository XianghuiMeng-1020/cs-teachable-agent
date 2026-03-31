def classify_hero(traits):
    strength = traits['strength']
    wisdom = traits['wisdom']
    courage = traits['courage']
    
    if strength > wisdom and strength > courage and strength > 50:
        return 'Warrior'
    elif wisdom > strength and wisdom > courage and wisdom > 50:
        return 'Seer'
    elif courage > strength and courage > wisdom and courage > 50:
        return 'Champion'
    else:
        return 'Unsung Hero'