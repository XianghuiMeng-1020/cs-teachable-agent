def translate_astronyms(astronyms, dictionary):
    return [dictionary.get(astryon, 'Unknown') for astryon in astronyms]