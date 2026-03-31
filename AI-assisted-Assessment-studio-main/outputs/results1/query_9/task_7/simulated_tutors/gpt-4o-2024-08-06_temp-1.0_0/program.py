def group_by_domain(characters):
    domain_dict = {}
    for character, domain in characters:
        if domain not in domain_dict:
            domain_dict[domain] = []
        domain_dict[domain].append(character)
    return domain_dict

# Test the function using the provided test cases
characters = [
    ['Zeus', 'Sky'],
    ['Poseidon', 'Sea'],
    ['Hades', 'Underworld'],
    ['Hera', 'Marriage'],
    ['Aphrodite', 'Love'],
    ['Ares', 'War'],
    ['Athena', 'Wisdom'],
    ['Hephaestus', 'Forge'],
    ['Demeter', 'Harvest'],
    ['Dionysus', 'Wine'],
    ['Hermes', 'Travel'],
    ['Artemis', 'Hunt'],
    ['Apollo', 'Sun'],
    ['Nyx', 'Night']
]

print(group_by_domain(characters) == {
    'Sky': ['Zeus'],
    'Sea': ['Poseidon'],
    'Underworld': ['Hades'],
    'Marriage': ['Hera'],
    'Love': ['Aphrodite'],
    'War': ['Ares'],
    'Wisdom': ['Athena'],
    'Forge': ['Hephaestus'],
    'Harvest': ['Demeter'],
    'Wine': ['Dionysus'],
    'Travel': ['Hermes'],
    'Hunt': ['Artemis'],
    'Sun': ['Apollo'],
    'Night': ['Nyx']
})