def assign_mythological_creature(zodiac_sign):
    # Dictionary mapping zodiac signs to mythological creatures
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
    
    # Return the mythological creature for the given zodiac sign
    # Use selection statement for unknown zodiac
    return creatures.get(zodiac_sign, "Unknown Creature")
