# Dropdown Question for decode_message

- Item ID: `task_7-dropdown`
- Item Type: `dropdown`
- Source Task: `task_7`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_7`

## Prompt
Fill each blank in the Python code with the single best option so the program matches the canonical source solution.

Source task summary:
### Task Description The Galactic Federation requires your programming prowess to help them decipher alien messages. You have intercepted encoded messages sent from different planets in the Andromeda Galaxy to Earth. Each intercepted message is a string containing words that correspond to specific planetary codes. Your task is to create a function `decode_message(galactic_message, codebook)` that takes in: - `galactic_message`: a string representing an encoded message. The words in the messag...

## Interaction Content
```python
def decode_message(__BLANK_3__, codebook):
    words = galactic_message.split()
    decoded_words = []
    for word in words:
        if word in codebook:
            decoded_words.append(codebook[word])
        else:
            decoded_words.append(__BLANK_1__)
    return __BLANK_2__.join(decoded_words)
```

### Blanks
- blank_1 (__BLANK_1__): `'UNKNOWN'`, `'MISSING'`, `'ERROR'`, `'INVALID'`
- blank_2 (__BLANK_2__): `' '`, `'UNKNOWN'`, `''`, `'TODO'`
- blank_3 (__BLANK_3__): `galactic_message`, `decode_message`, `codebook`, `words`

## Answer Key
```json
{
  "correct_answers": {
    "blank_1": "'UNKNOWN'",
    "blank_2": "' '",
    "blank_3": "galactic_message"
  }
}
```

## Grading Rule
Each blank has exactly one credited option. Award full credit only if every blank is correct.

## Validation
- Passed: `True`