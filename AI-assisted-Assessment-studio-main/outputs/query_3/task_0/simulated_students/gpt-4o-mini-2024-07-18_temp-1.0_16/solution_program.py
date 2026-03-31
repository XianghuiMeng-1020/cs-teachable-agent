def translate_astronyms(astronyms, dictionary):
    return [dictionary.get(astronym, 'Unknown') for astronym in astronyms]