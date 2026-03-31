def god_info(god_name):
    gods = {
        "zeus": {"domain": "Sky and Thunder", "symbol": "Thunderbolt"},
        "poseidon": {"domain": "Sea", "symbol": "Trident"},
        "hades": {"domain": "Underworld", "symbol": "Helmet of invisibility"},
        "ares": {"domain": "War", "symbol": "Spear"},
        "aphrodite": {"domain": "Love", "symbol": "Dove"},
        "athena": {"domain": "Wisdom", "symbol": "Owl"}
    }
    g_info = gods.get(god_name.lower())
    if g_info:
        return f"Domain: {g_info['domain']}, Symbol: {g_info['symbol']}"
    else:
        return "Unknown god"