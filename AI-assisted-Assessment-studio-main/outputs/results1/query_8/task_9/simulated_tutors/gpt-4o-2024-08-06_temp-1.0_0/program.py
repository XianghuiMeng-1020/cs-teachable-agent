def mythical_character_power(character_name):
    # Define a dictionary with character names as keys and their powers as values
    character_powers = {
        'Zeus': 'Thunder',
        'Poseidon': 'Sea',
        'Hades': 'Underworld',
        'Athena': 'Wisdom',
        'Apollo': 'Sun'
    }
    # Look up the character name in the dictionary and return the corresponding power,
    # or return 'Unknown' if the character is not found
    return character_powers.get(character_name, 'Unknown')