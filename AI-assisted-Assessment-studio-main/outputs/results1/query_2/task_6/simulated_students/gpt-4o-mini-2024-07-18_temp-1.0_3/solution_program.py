import random


def generate_slots(num_slots, word_list):
    return ' '.join(random.choice(word_list) for _ in range(num_slots))


def determine_outcome(slot_str):
    slots = slot_str.split()  
    return 'WIN' if len(set(slots)) == 1 else 'LOSE'


def read_words_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]  


def spin_and_check(filename, num_slots):
    words = read_words_from_file(filename)
    slots_result = generate_slots(num_slots, words)
    return determine_outcome(slots_result)