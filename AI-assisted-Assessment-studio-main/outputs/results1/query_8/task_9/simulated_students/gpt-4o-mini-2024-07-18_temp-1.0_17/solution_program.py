def mythical_character_power(character_name):
    characters = {
        'Zeus': 'Thunder',
        'Poseidon': 'Sea',
        'Hades': 'Underworld',
        'Athena': 'Wisdom',
        'Apollo': 'Sun'
    }
    return characters.get(character_name, 'Unknown')