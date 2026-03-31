def decode_message(code, translation_rules):
    total_sum = 0
    for char in code:
        if char in translation_rules:
            total_sum += translation_rules[char]
        else:
            total_sum += 0
    return total_sum