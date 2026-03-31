def mythical_character_power(character_name):
    powers = {
        'Zeus': 'Thunder',
        'Poseidon': 'Sea',
        'Hades': 'Underworld',
        'Athena': 'Wisdom',
        'Apollo': 'Sun'
    }
    return powers.get(character_name, 'Unknown')