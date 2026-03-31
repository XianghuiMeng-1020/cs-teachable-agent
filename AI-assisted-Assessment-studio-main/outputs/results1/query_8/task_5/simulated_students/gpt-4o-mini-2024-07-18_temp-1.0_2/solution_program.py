def god_info(god_name):
    gods = {
        'zeus': {'domain': 'Sky and Thunder', 'symbol': 'Thunderbolt'},
        'poseidon': {'domain': 'Sea', 'symbol': 'Trident'},
        'hades': {'domain': 'Underworld', 'symbol': 'Helmet of invisibility'},
        'ares': {'domain': 'War', 'symbol': 'Spear'},
        'aphrodite': {'domain': 'Love', 'symbol': 'Dove'},
        'athena': {'domain': 'Wisdom', 'symbol': 'Owl'}
    }
    god_name_lower = god_name.lower()
    if god_name_lower in gods:
        god = gods[god_name_lower]
        return f'Domain: {god['domain']}, Symbol: {god['symbol']}'
    else:
        return 'Unknown god'