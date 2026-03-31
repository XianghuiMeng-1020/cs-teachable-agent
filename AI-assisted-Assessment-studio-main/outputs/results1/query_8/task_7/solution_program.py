def describe_god(name):
    god_domains = {
        "zeus": "God of the sky and thunder",
        "poseidon": "God of the sea",
        "hades": "God of the underworld",
        "athena": "Goddess of wisdom and war",
        "apollo": "God of the sun and music",
        "artemis": "Goddess of the hunt and moon",
        "ares": "God of war",
        "demeter": "Goddess of the harvest",
        "hera": "Goddess of marriage"
    }
    name_lower = name.lower()
    if name_lower in god_domains:
        return god_domains[name_lower]
    else:
        return "Unknown god"