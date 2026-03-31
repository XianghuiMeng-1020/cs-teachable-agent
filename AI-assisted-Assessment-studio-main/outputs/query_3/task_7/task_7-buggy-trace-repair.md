# Buggy Trace Repair for decode_message

- Item ID: `task_7-buggy-trace-repair`
- Item Type: `buggy-trace-repair`
- Source Task: `task_7`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_7`

## Prompt
The Python function below contains a single bug. The displayed checkpoint values come from running the buggy version of the function. Repair the trace by writing the value each named variable should have after the bug is fixed.

Function: decode_message
Concrete call: decode_message('QXZ BFO GAO', {'QXZ': 'hello', 'BFO': 'world', 'DZT': 'alien'})

Source task summary:
### Task Description The Galactic Federation requires your programming prowess to help them decipher alien messages. You have intercepted encoded messages sent from different planets in the Andromeda Galaxy to Earth. Each intercepted message is a string containing words that correspond to specific planetary codes. Your task is to create a function `decode_message(galactic_message, codebook)` that takes in: - `galactic_message`: a string representing an encoded message. The words in the messag...

## Interaction Content
- Function: `decode_message`
- Concrete Call: `decode_message('QXZ BFO GAO', {'QXZ': 'hello', 'BFO': 'world', 'DZT': 'alien'})`

### Buggy Function Source
```python
def decode_message(galactic_message, codebook):
    words = galactic_message.split()
    decoded_words = []
    for word in words:
        if word in codebook:
            decoded_words.extend(codebook[word])
        else:
            decoded_words.append('UNKNOWN')
    return ' '.join(decoded_words)
```

### Repair Checkpoints
- `checkpoint_1`: after line 6 (`            decoded_words.append(codebook[word])`), buggy `decoded_words` = `['h', 'e', 'l', 'l', 'o']`
- `checkpoint_2`: after line 6 (`            decoded_words.append(codebook[word])`), buggy `decoded_words` = `['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']`
- `checkpoint_3`: after line 8 (`            decoded_words.append('UNKNOWN')`), buggy `decoded_words` = `['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd', 'UNKNOWN']`

## Answer Key
```json
{
  "corrected_answers": {
    "checkpoint_1": "['hello']",
    "checkpoint_2": "['hello', 'world']",
    "checkpoint_3": "['hello', 'world', 'UNKNOWN']"
  },
  "correct_function_source": "def decode_message(galactic_message, codebook):\n    words = galactic_message.split()\n    decoded_words = []\n    for word in words:\n        if word in codebook:\n            decoded_words.append(codebook[word])\n        else:\n            decoded_words.append('UNKNOWN')\n    return ' '.join(decoded_words)",
  "buggy_line_number": 6,
  "buggy_source_line": "decoded_words.extend(codebook[word])",
  "mutation_label": "append_to_extend"
}
```

## Grading Rule
Award full credit only when every checkpoint is repaired to the canonical value produced by the corrected program.

## Validation
- Passed: `True`