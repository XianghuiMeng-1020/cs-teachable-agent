import random

def generate_slots(num_slots, word_list):
    return ' '.join(random.choice(word_list) for _ in range(num_slots))

def determine_outcome(slot_str):
    slots = slot_str.split()
    return 'WIN' if all(slot == slots[0] for slot in slots) else 'LOSE'

def read_words_from_file(filename):
    with open(filename) as file:
        return file.read().splitlines()

def spin_and_check(filename, num_slots):
    word_list = read_words_from_file(filename)
    result = generate_slots(num_slots, word_list)
    return determine_outcome(result)