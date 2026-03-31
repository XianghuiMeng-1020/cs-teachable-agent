def assign_mythological_creature(zodiac_sign):
    zodiac_to_creature = {
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
    return zodiac_to_creature.get(zodiac_sign, 'Unknown Creature')