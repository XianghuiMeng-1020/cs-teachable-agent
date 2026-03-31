# Dropdown Question for luckiest_player

- Item ID: `task_4-dropdown`
- Item Type: `dropdown`
- Source Task: `task_4`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_0/task_4`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
### Luckiest Player of the Day In a casino themed on Games of Chance, players enjoy slot machines. Each day, the casino logs the wins of players in a text file named `daily_wins.txt`. Your task is to determine the 'Luckiest Player of the Day', meaning the player with the highest total winnings on that day. The log file, `daily_wins.txt`, will have the following format: - Each line contains a player's name followed by a space, and then their winnings as an integer. A player can appear multiple...

## Interaction Content
```python
def luckiest_player(filename):
    with open(filename, 'r') as file:
        player_totals = {}
        for line in file:
            name, winnings = line.rsplit(maxsplit=__BLANK_3__)
            winnings = int(winnings)
            if name in player_totals:
                player_totals[name] += winnings
            else:
                player_totals[name] = winnings
        max_winnings = __BLANK_1__float('inf')
        luckiest = None
        for player in sorted(player_totals):
            if player_totals[player] __BLANK_2__ max_winnings:
                max_winnings = player_totals[player]
                luckiest = player
        return luckiest
```

### Blanks
- blank_1 (__BLANK_1__): `-`, `+`, `*`, `%`
- blank_2 (__BLANK_2__): `>`, `>=`, `<`, `<=`
- blank_3 (__BLANK_3__): `1`, `2`, `0`, `3`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "-",
    "blank_2": ">",
    "blank_3": "1"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`