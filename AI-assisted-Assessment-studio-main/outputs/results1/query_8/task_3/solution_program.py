def assign_mythological_creature(zodiac_sign):
    creatures = {
        'Aries': 'Dragon',
        'Taurus': 'Minotaur',
        'Gemini': 'Griffin',
        'Cancer': 'Cyclops',
        'Leo': 'Phoenix',
        'Virgo': 'Sphinx',
        'Libra': 'Centaur',
        'Scorpio': 'Hydra',
        'Sagittarius': 'Pegasus',
        'Capricorn': 'Leviathan',
        'Aquarius': 'Kraken',
        'Pisces': 'Mermaid'
    }
    if zodiac_sign in creatures:
        return creatures[zodiac_sign]
    else:
        return "Unknown Creature"