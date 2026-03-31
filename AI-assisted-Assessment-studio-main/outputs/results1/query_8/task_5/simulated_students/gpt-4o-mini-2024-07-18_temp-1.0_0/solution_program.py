def god_info(god_name):
    gods = {
        'zeus': {'domain': 'Sky and Thunder', 'symbol': 'Thunderbolt'},
        'poseidon': {'domain': 'Sea', 'symbol': 'Trident'},
        'hades': {'domain': 'Underworld', 'symbol': 'Helmet of invisibility'},
        'ares': {'domain': 'War', 'symbol': 'Spear'},
        'aphrodite': {'domain': 'Love', 'symbol': 'Dove'},
        'athena': {'domain': 'Wisdom', 'symbol': 'Owl'}
    }
    god_name = god_name.lower()
    if god_name in gods:
        domain = gods[god_name]['domain']
        symbol = gods[god_name]['symbol']
        return f'Domain: {domain}, Symbol: {symbol}'
    else:
        return 'Unknown god'