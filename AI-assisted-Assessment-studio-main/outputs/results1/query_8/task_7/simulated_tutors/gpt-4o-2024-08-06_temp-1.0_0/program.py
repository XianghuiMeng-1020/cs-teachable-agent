def describe_god(name):
    # Define a dictionary mapping god names to their domains
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
    
    # Convert the input name to lowercase for case insensitive matching
    name_lower = name.lower()
    
    # Use a selection statement to find the domain of the god
    if name_lower in gods:
        return gods[name_lower]
    else:
        return "Unknown god"