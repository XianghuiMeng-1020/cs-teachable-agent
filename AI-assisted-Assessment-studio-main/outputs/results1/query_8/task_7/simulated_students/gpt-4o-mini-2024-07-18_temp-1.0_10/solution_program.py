def describe_god(name):
    name = name.strip().capitalize()
    domains = {
        'Zeus': 'God of the sky and thunder',
        'Poseidon': 'God of the sea',
        'Hades': 'God of the underworld',
        'Athena': 'Goddess of wisdom and war',
        'Apollo': 'God of the sun and music',
        'Artemis': 'Goddess of the hunt and moon',
        'Ares': 'God of war',
        'Demeter': 'Goddess of the harvest',
        'Hera': 'Goddess of marriage'
    }
    return domains.get(name, 'Unknown god')