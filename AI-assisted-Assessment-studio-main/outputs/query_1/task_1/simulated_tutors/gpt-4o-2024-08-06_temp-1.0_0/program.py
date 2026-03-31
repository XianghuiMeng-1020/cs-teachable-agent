def mythical_quest(heroes, total_artifacts):
    # Define artifact allocation per rank
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    
    # Prepare the result list and reduce remaining artifacts as heroes are allocated
    result = []
    remaining_artifacts = total_artifacts
    
    # Allocate artifacts by rank priority: Advanced, Intermediate, Novice
    for hero, rank in heroes:
        artifacts_needed = rank_to_artifacts[rank]
        if remaining_artifacts >= artifacts_needed:
            result.append((hero, artifacts_needed))
            remaining_artifacts -= artifacts_needed
        else:
            result.append((hero, 0))
    
    return result

# Test the program with the given suite
if __name__ == "__main__":
    # Include the test cases here or use pytest as defined in the task
    assert mythical_quest([
        ['Ares', 'Advanced'],
        ['Perseus', 'Intermediate'],
        ['Hercules', 'Novice']
    ], 10) == [('Ares', 7), ('Perseus', 3), ('Hercules', 0)]
    
    assert mythical_quest([
        ['Zeus', 'Advanced'],
        ['Athena', 'Intermediate'],
        ['Apollo', 'Intermediate'],
        ['Hermes', 'Novice']
    ], 20) == [('Zeus', 7), ('Athena', 3), ('Apollo', 3), ('Hermes', 1)]

    assert mythical_quest([
        ['Hades', 'Advanced'],
        ['Artemis', 'Intermediate'],
        ['Dionysus', 'Novice']
    ], 11) == [('Hades', 7), ('Artemis', 3), ('Dionysus', 1)]

    assert mythical_quest([
        ['Hera', 'Advanced'],
        ['Demeter', 'Advanced'],
        ['Ares', 'Intermediate']
    ], 14) == [('Hera', 7), ('Demeter', 7), ('Ares', 0)]

    assert mythical_quest([
        ['Helios', 'Novice']
    ], 5) == [('Helios', 1)]