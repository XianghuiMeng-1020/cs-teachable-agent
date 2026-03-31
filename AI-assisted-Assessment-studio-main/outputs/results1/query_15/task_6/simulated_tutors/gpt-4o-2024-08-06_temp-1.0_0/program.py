def decode_alien_message(message):
    decoded_values = []
    for char in message:
        # Convert each character to its corresponding alphabet position
        decoded_value = ord(char) - ord('a') + 1
        decoded_values.append(decoded_value)
    return decoded_values

# Example usage:
# message = "abc"
# print(decode_alien_message(message))  # Output: [1, 2, 3]