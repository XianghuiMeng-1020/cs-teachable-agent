def god_info(god_name):
    gods = {
        "zeus": {"Domain": "Sky and Thunder", "Symbol": "Thunderbolt"},
        "poseidon": {"Domain": "Sea", "Symbol": "Trident"},
        "hades": {"Domain": "Underworld", "Symbol": "Helmet of invisibility"},
        "ares": {"Domain": "War", "Symbol": "Spear"},
        "aphrodite": {"Domain": "Love", "Symbol": "Dove"},
        "athena": {"Domain": "Wisdom", "Symbol": "Owl"}
    }
    god_name_lower = god_name.lower()
    if god_name_lower in gods:
        god_data = gods[god_name_lower]
        return f"Domain: {god_data['Domain']}, Symbol: {god_data['Symbol']}"
    else:
        return "Unknown god"