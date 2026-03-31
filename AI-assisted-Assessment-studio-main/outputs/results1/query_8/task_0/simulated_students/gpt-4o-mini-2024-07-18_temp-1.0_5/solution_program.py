def identify_god(domain):
    gods = {
        'war': 'Ares',
        'wisdom': 'Athena',
        'love': 'Aphrodite',
        'underworld': 'Hades',
        'thunder': 'Zeus'
    }
    return gods.get(domain, 'Unknown')
