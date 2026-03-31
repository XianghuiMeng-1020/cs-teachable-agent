def decode_message(code, translation_rules):
    total = 0
    for char in code:
        total += translation_rules.get(char, 0)
    return total