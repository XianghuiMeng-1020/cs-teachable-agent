def classify_hero(traits):
    max_trait = max(traits, key=traits.get)
    if max_trait == 'strength' and traits[max_trait] > 50:
        return 'Warrior'
    elif max_trait == 'wisdom' and traits[max_trait] > 50:
        return 'Seer'
    elif max_trait == 'courage' and traits[max_trait] > 50:
        return 'Champion'
    else:
        return 'Unsung Hero'