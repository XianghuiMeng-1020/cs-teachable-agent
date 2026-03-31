def god_info(god_name):
    gods = {
        'zeus': {'domain': 'Sky and Thunder', 'symbol': 'Thunderbolt'},
        'poseidon': {'domain': 'Sea', 'symbol': 'Trident'},
        'hades': {'domain': 'Underworld', 'symbol': 'Helmet of invisibility'},
        'ares': {'domain': 'War', 'symbol': 'Spear'},
        'aphrodite': {'domain': 'Love', 'symbol': 'Dove'},
        'athena': {'domain': 'Wisdom', 'symbol': 'Owl'}
    }
    god_key = god_name.lower()
    if god_key in gods:
        domain = gods[god_key]['domain']
        symbol = gods[god_key]['symbol']
        return f'Domain: {domain}, Symbol: {symbol}'
    else:
        return 'Unknown god'