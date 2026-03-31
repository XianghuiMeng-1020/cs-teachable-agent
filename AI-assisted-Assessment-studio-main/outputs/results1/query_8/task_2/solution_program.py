def classify_creature(creature):
    creatures = {
        'Phoenix': 'sky',
        'Garuda': 'sky',
        'Thunderbird': 'sky',
        'Kraken': 'sea',
        'Leviathan': 'sea',
        'Mermaid': 'sea',
        'Golem': 'earth',
        'Satyr': 'earth',
        'Nymph': 'earth'
    }
    if creature in creatures:
        return creatures[creature]
    else:
        return 'other'