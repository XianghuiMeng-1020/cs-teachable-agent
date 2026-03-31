def classify_creature(creature):
    categories = {
        'sky': ['Phoenix', 'Garuda', 'Thunderbird'],
        'sea': ['Kraken', 'Leviathan', 'Mermaid'],
        'earth': ['Golem', 'Satyr', 'Nymph']
    }
    
    for domain, creatures in categories.items():
        if creature in creatures:
            return domain
    
    return 'other'