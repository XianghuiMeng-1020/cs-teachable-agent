def decode_message(code, translation_rules):
    total_sum = 0
    for char in code:
        # Get the coordinate value; default to 0 if character not in translation_rules
        coordinate = translation_rules.get(char, 0)
        # Add the coordinate to the total sum
        total_sum += coordinate
    return total_sum

# Test cases
print(decode_message("ABCAAA", {'A': 10, 'B': 5, 'C': 2})) # Output should be 39
print(decode_message("XXYYZ", {'X': 3, 'Y': 4}))          # Output should be 14
print(decode_message("", {'A': 1}))                        # Output should be 0
print(decode_message("ZZZZ", {'Z': 0}))                   # Output should be 0
print(decode_message("PTQ", {}))                           # Output should be 0