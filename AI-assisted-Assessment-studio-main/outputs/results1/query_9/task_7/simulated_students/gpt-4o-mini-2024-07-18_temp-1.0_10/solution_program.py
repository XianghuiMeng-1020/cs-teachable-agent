def group_by_domain(characters):
    domain_dict = {}
    for character, domain in characters:
        if domain not in domain_dict:
            domain_dict[domain] = []
        domain_dict[domain].append(character)
    return domain_dict