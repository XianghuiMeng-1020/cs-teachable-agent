import random

# Task 1: generate_slots function
def generate_slots(num_slots, word_list):
    return ' '.join(random.choice(word_list) for _ in range(num_slots))

# Task 2: determine_outcome function
def determine_outcome(slot_str):
    words = slot_str.split()
    return 'WIN' if all(word == words[0] for word in words) else 'LOSE'

# Task 3: read_words_from_file function
def read_words_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Task 4: spin_and_check function
def spin_and_check(filename, num_slots):
    word_list = read_words_from_file(filename)
    slots_outcome = generate_slots(num_slots, word_list)
    return determine_outcome(slots_outcome)
