def mythical_character_power(character_name):
    character_powers = {
        'Zeus': 'Thunder',
        'Poseidon': 'Sea',
        'Hades': 'Underworld',
        'Athena': 'Wisdom',
        'Apollo': 'Sun'
    }
    return character_powers.get(character_name, 'Unknown')