def classify_creature(creature):
    # Dictionary categorizing creatures by their domains
    creature_domains = {
        'sky': ['Phoenix', 'Garuda', 'Thunderbird'],
        'sea': ['Kraken', 'Leviathan', 'Mermaid'],
        'earth': ['Golem', 'Satyr', 'Nymph'],
    }

    # Iterate through the dictionary to find the creature's domain
    for domain, creatures in creature_domains.items():
        if creature in creatures:
            return domain
    
    # If the creature is not found in any domain, return 'other'
    return 'other'