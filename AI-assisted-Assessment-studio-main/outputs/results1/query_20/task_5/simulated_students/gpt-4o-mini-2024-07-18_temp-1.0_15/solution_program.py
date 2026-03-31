def calculate_score(settlementsA, settlementsB, specialLocations):
    def count_adjacent_settlements(settlements, special):
        score = 0
        for i in range(len(settlements)):
            if special[i] == 'S':
                if i > 0 and settlements[i - 1] == '1':
                    score += 1
                if i < len(settlements) - 1 and settlements[i + 1] == '1':
                    score += 1
        return score

    scoreA = count_adjacent_settlements(settlementsA, specialLocations)
    scoreB = count_adjacent_settlements(settlementsB, specialLocations)

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'