# Dropdown Question for classify_planets

- Item ID: `task_4-dropdown`
- Item Type: `dropdown`
- Source Task: `task_4`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_4`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
**Task Description:** In the distant future, the Galactic Institute of Astronomical Studies is classifying various planets in the galaxy based on their atmospheric density and the presence of alien lifeforms. You have been tasked to write a Python function, `classify_planets(data)`, that takes a list of planets as its argument. Each planet is represented as a dictionary containing the following keys: - `name`: A string representing the planet's name. - `atmos_density`: A float value represent...

## Interaction Content
```python
def classify_planets(data):
    categories = {
        'Habitable': [],
        'Potentially Habitable': [],
        'Uninhabitable': []
    }
    for planet in data:
        density = planet['atmos_density']
        life = planet['alien_life']
        name = planet['name']
        if __BLANK_3__ __BLANK_1__ density __BLANK_2__ 3.0:
            if life:
                categories['Habitable'].append(name)
            else:
                categories['Potentially Habitable'].append(name)
        else:
            categories['Uninhabitable'].append(name)
    return categories
```

### Blanks
- blank_1 (__BLANK_1__): `<=`, `<`, `>=`, `>`
- blank_2 (__BLANK_2__): `<=`, `<`, `>=`, `>`
- blank_3 (__BLANK_3__): `1.0`, `0`, `1`, `2`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "<=",
    "blank_2": "<=",
    "blank_3": "1.0"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`