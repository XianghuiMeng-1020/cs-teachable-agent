def mythical_character_power(character_name):
    powers = {
        'Zeus': 'Thunder',
        'Poseidon': 'Sea',
        'Hades': 'Underworld',
        'Athena': 'Wisdom',
        'Apollo': 'Sun'
    }
    if character_name in powers:
        return powers[character_name]
    else:
        return 'Unknown'