# Dropdown Question for calculate_scores

- Item ID: `task_0-dropdown`
- Item Type: `dropdown`
- Source Task: `task_0`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_4/task_0`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
### Task Description: You are part of a team developing a board game scoring system. Each player in the board game has both positive and negative scores collected during gameplay. You need to write a Python program that calculates and returns the total score of each player. Your program should define a function `calculate_scores(player_scores)` that takes in a dictionary, `player_scores`, where the keys are strings representing player names, and the values are lists of integers representing t...

## Interaction Content
```python
def calculate_scores(__BLANK_2__):
    __BLANK_3__ = {}
    for player, scores in player_scores.items():
        total = __BLANK_1__
        for score in scores:
            total += score
        total_scores[player] = total
    return total_scores
```

### Blanks
- blank_1 (__BLANK_1__): `0`, `1`, `-1`, `2`
- blank_2 (__BLANK_2__): `player_scores`, `calculate_scores`, `total_scores`, `player`
- blank_3 (__BLANK_3__): `total_scores`, `calculate_scores`, `player_scores`, `player`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "0",
    "blank_2": "player_scores",
    "blank_3": "total_scores"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`