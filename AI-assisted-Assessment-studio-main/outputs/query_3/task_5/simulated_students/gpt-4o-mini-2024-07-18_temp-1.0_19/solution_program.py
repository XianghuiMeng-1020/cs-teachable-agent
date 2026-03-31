def decode_message(code, translation_rules):
    total_sum = 0
    for char in code:
        total_sum += translation_rules.get(char, 0)
    return total_sum