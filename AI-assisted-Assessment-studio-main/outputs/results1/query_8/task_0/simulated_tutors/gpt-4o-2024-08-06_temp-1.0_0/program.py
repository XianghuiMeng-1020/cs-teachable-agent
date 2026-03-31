def identify_god(domain):
    gods = {
        'war': 'Ares',
        'wisdom': 'Athena',
        'love': 'Aphrodite',
        'underworld': 'Hades',
        'thunder': 'Zeus'
    }
    return gods.get(domain, 'Unknown')

# Test cases
print(identify_god('war'))       # Should print 'Ares'
print(identify_god('thunder'))   # Should print 'Zeus'
print(identify_god('water'))     # Should print 'Unknown'
print(identify_god('wisdom'))    # Should print 'Athena'
print(identify_god('underworld'))# Should print 'Hades'