def identify_god(domain):
    gods = {
        'war': 'Ares',
        'wisdom': 'Athena',
        'love': 'Aphrodite',
        'underworld': 'Hades',
        'thunder': 'Zeus'
    }
    if domain in gods:
        return gods[domain]
    else:
        return 'Unknown'