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
        return f"Domain: {gods[god_name]['domain']}, Symbol: {gods[god_name]['symbol']}"
    else:
        return "Unknown god"