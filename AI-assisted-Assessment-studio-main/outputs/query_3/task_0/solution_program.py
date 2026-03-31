def translate_astronyms(astronyms, dictionary):
    translated = []
    for astronym in astronyms:
        if astronym in dictionary:
            translated.append(dictionary[astronym])
        else:
            translated.append('Unknown')
    return translated