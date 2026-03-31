def board_game_summary(results):
    import re
    pattern = re.compile(r'([A-Z])(\d+)')
    score_dict = {}

    for match in pattern.finditer(results):
        player = match.group(1)
        score = int(match.group(2))

        if player in score_dict:
            score_dict[player] += score
        else:
            score_dict[player] = score

    for i in range(len(results)):
        if not (results[i].isalpha() and results[i].isupper()) and (results[i].isdigit() or results[i] == ''):
            raise ValueError(f'Invalid character or format in results string at position {i}: {results[i]}')

    return score_dict