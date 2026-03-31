def group_by_domain(characters):
    domain_dict = {}
    for character, domain in characters:
        if domain in domain_dict:
            domain_dict[domain].append(character)
        else:
            domain_dict[domain] = [character]
    return domain_dict