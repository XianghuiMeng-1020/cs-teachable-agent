def describe_god(name):
    name = name.lower()
    gods = {
        'zeus': "God of the sky and thunder",
        'poseidon': "God of the sea",
        'hades': "God of the underworld",
        'athena': "Goddess of wisdom and war",
        'apollo': "God of the sun and music",
        'artemis': "Goddess of the hunt and moon",
        'ares': "God of war",
        'demeter': "Goddess of the harvest",
        'hera': "Goddess of marriage"
    }
    return gods.get(name, "Unknown god")