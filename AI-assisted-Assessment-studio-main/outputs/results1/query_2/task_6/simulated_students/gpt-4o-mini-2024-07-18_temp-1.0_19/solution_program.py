import random


def generate_slots(num_slots, word_list):
    slots = random.choices(word_list, k=num_slots)
    return ' '.join(slots)


def determine_outcome(slot_str):
    outcomes = slot_str.split()
    return 'WIN' if len(set(outcomes)) == 1 else 'LOSE'


def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    return words


def spin_and_check(filename, num_slots):
    words = read_words_from_file(filename)
    slot_result = generate_slots(num_slots, words)
    return determine_outcome(slot_result)