def assign_mythological_creature(zodiac_sign):
    zodiac_creatures = {
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
    return zodiac_creatures.get(zodiac_sign, 'Unknown Creature')