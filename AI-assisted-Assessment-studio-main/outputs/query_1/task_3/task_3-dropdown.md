# Dropdown Question for calculate_awards

- Item ID: `task_3-dropdown`
- Item Type: `dropdown`
- Source Task: `task_3`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_1/task_3`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
**Task: Valhalla Warriors Calculation** In Norse mythology, warriors who die in combat are taken to Valhalla, where they become einherjar and train for the events of Ragnarok. We're interested in creating a program to keep track of these warriors and award them based on their achievements. Write a function `calculate_awards(warrior_achievements)` that takes a list of integers, `warrior_achievements`, where each integer represents the number of successful combats a warrior has won. You need to...

## Interaction Content
```python
def calculate_awards(warrior_achievements):
    awards = []
    for achievements in warrior_achievements:
        if achievements __BLANK_1__ 0:
            awards.append('Novice')
        elif __BLANK_2__ <= achievements <= 5:
            awards.append('Adept')
        elif __BLANK_3__ <= achievements <= 10:
            awards.append('Veteran')
        else:
            awards.append('Elite')
    return awards
```

### Blanks
- blank_1 (__BLANK_1__): `==`, `!=`, `<`, `>`
- blank_2 (__BLANK_2__): `1`, `2`, `0`, `3`
- blank_3 (__BLANK_3__): `6`, `7`, `5`, `8`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "==",
    "blank_2": "1",
    "blank_3": "6"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`