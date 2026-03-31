def classify_creature(creature):
    creature_categories = {
        'sky': ['Phoenix', 'Garuda', 'Thunderbird'],
        'sea': ['Kraken', 'Leviathan', 'Mermaid'],
        'earth': ['Golem', 'Satyr', 'Nymph']
    }
    
    for domain, creatures in creature_categories.items():
        if creature in creatures:
            return domain
    
    return 'other'