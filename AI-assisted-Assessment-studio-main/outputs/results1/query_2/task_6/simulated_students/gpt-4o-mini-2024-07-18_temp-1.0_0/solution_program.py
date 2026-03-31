import random

def generate_slots(num_slots, word_list):
    slots = random.choices(word_list, k=num_slots)
    return ' '.join(slots)


def determine_outcome(slot_str):
    slots = slot_str.split()
    if all(slot == slots[0] for slot in slots):
        return 'WIN'
    return 'LOSE'


def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words


def spin_and_check(filename, num_slots):
    words = read_words_from_file(filename)
    result = generate_slots(num_slots, words)
    return determine_outcome(result)