def god_info(god_name):
    gods = {
        'zeus': {'Domain': 'Sky and Thunder', 'Symbol': 'Thunderbolt'},
        'poseidon': {'Domain': 'Sea', 'Symbol': 'Trident'},
        'hades': {'Domain': 'Underworld', 'Symbol': 'Helmet of invisibility'},
        'ares': {'Domain': 'War', 'Symbol': 'Spear'},
        'aphrodite': {'Domain': 'Love', 'Symbol': 'Dove'},
        'athena': {'Domain': 'Wisdom', 'Symbol': 'Owl'}
    }
    god_name = god_name.lower()
    if god_name in gods:
        domain = gods[god_name]['Domain']
        symbol = gods[god_name]['Symbol']
        return f'Domain: {domain}, Symbol: {symbol}'
    else:
        return 'Unknown god'