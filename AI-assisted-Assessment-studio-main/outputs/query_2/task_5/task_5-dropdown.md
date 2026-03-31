# Dropdown Question for sort_ingredients

- Item ID: `task_5-dropdown`
- Item Type: `dropdown`
- Source Task: `task_5`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_2/task_5`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
## Task: Recipe Ingredient Sorter Your task is to create a program that reads a text file containing ingredients of various recipes, sorts the ingredients alphabetically, and saves the sorted list back into a new file. ### File Format: - Each line in the file contains ingredients of one recipe separated by commas. - There are no headers or labels in the file. ### Program Requirements: 1. Implement a function `sort_ingredients(input_filename, output_filename)` where: - `input_filename` is the ...

## Interaction Content
```python
def sort_ingredients(input_filename, output_filename):
    with open(input_filename, __BLANK_2__) as f:
        lines = f.readlines()

    sorted_lines = []
    for line in lines:
        ingredients = line.strip().split(__BLANK_3__)
        ingredients = [ingredient.strip() for ingredient in ingredients]
        ingredients.sort()
        sorted_line = ', '.join(ingredients)
        sorted_lines.append(sorted_line)

    with open(output_filename, 'w') as f:
        for sorted_line in sorted_lines:
            f.write(sorted_line __BLANK_1__ '\n')
```

### Blanks
- blank_1 (__BLANK_1__): `+`, `-`, `*`, `%`
- blank_2 (__BLANK_2__): `'r'`, `'UNKNOWN'`, `''`, `'TODO'`
- blank_3 (__BLANK_3__): `','`, `'UNKNOWN'`, `''`, `'TODO'`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "+",
    "blank_2": "'r'",
    "blank_3": "','"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`