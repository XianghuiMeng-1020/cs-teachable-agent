def translate_astronyms(astronyms, dictionary):
    return [dictionary.get(astrynom, 'Unknown') for astrynom in astronyms]