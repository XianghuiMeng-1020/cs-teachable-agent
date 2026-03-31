def board_game_summary(results):
    if not results:
        raise ValueError("Invalid format in results string")
    
    from collections import defaultdict
    import re

    # Regex to match valid patterns
    pattern = re.compile(r"([A-Z])(\d+)")
    players_scores = defaultdict(int)

    pos = 0
    while pos < len(results):
        match = pattern.match(results, pos)
        if not match:
            raise ValueError("Invalid format in results string")
        player, score = match.groups()
        players_scores[player] += int(score)
        pos = match.end()

    return dict(players_scores)

def tests():  # Run only a few quick tests
    assert board_game_summary("A12B4A3B10C1") == {'A': 15, 'B': 14, 'C': 1}
    assert board_game_summary("Z50") == {'Z': 50}
    assert board_game_summary("D2D3D5") == {'D': 10}
    try:
        board_game_summary("E3F2GZ")
    except ValueError as e:
        assert str(e) == "Invalid format in results string"
    try:
        board_game_summary("")
    except ValueError as e:
        assert str(e) == "Invalid format in results string"

# Uncomment to run tests
tests()