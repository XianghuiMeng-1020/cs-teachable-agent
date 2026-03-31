def translate_astronyms(astronyms, dictionary):
    translated = []
    for astronym in astronyms:
        if astronym in dictionary:
            translated.append(dictionary[astronym])
        else:
            translated.append("Unknown")
    return translated

# Example usage:
# astronyms = ['xer', 'unknown', 'gicon', 'zuru']
# dictionary = {'xer': 'Star', 'gicon': 'Nebula'}
# print(translate_astronyms(astronyms, dictionary))