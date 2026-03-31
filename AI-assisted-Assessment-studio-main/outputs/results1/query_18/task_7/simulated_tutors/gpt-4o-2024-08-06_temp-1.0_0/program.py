def calculate_total_distance(filename):
    total_distance = 0
    with open(filename, 'r') as file:
        for line in file:
            _, distance = line.split()
            total_distance += int(float(distance))
    return total_distance

# Evaluating context relevance
# Theme: Science Fiction
# The task involves reading distances (related to space/planets)
# Method: Through file handling, use of variables, and arithmetic operations
context_relevance = 1 # Because all concepts are used, and the theme is represented through the sci-fi context.