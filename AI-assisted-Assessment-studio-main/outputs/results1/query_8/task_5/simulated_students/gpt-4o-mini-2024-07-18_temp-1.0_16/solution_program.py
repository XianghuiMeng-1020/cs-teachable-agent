def god_info(god_name):
    gods = {
        'zeus': {'Domain': 'Sky and Thunder', 'Symbol': 'Thunderbolt'},
        'poseidon': {'Domain': 'Sea', 'Symbol': 'Trident'},
        'hades': {'Domain': 'Underworld', 'Symbol': 'Helmet of invisibility'},
        'ares': {'Domain': 'War', 'Symbol': 'Spear'},
        'aphrodite': {'Domain': 'Love', 'Symbol': 'Dove'},
        'athena': {'Domain': 'Wisdom', 'Symbol': 'Owl'}
    }
    god_name_lower = god_name.lower()
    if god_name_lower in gods:
        domain = gods[god_name_lower]['Domain']
        symbol = gods[god_name_lower]['Symbol']
        return f'Domain: {domain}, Symbol: {symbol}'
    else:
        return 'Unknown god'