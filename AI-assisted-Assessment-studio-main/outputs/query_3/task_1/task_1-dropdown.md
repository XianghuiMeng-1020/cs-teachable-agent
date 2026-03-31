# Dropdown Question for sort_space_stations

- Item ID: `task_1-dropdown`
- Item Type: `dropdown`
- Source Task: `task_1`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_1`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
### Task Description In a futuristic interstellar society, space stations are assigned numbers indicating their position along the cosmic trail. The numbers are sequenced such that `Even` numbered stations belong to the alien Teklar species, while `Odd` numbered stations are inhabited by humans. The task is to create a function `sort_space_stations(stations)` that takes a dictionary of space stations and sorts them based on their numbering. #### Input: - A dictionary `stations` where keys are...

## Interaction Content
```python
def sort_space_stations(stations):
    sorted_stations = {}
    for key in sorted(stations.keys()):
        prefix = 'Teklar' if key __BLANK_1__ __BLANK_3__ __BLANK_2__ 0 else 'Human'
        new_key = f"{prefix} {key}"
        sorted_stations[new_key] = stations[key]
    return sorted_stations
```

### Blanks
- blank_1 (__BLANK_1__): `%`, `//`, `+`, `-`
- blank_2 (__BLANK_2__): `==`, `!=`, `<`, `>`
- blank_3 (__BLANK_3__): `2`, `3`, `1`, `0`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "%",
    "blank_2": "==",
    "blank_3": "2"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`