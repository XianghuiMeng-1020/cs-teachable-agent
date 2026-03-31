# Parsons Problem for decode_message

- Item ID: `task_7-parsons`
- Item Type: `parsons`
- Source Task: `task_7`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_7`

## Prompt
Reorder the scrambled Python code blocks so they reconstruct the correct solution for the source task.

Source task summary:
### Task Description The Galactic Federation requires your programming prowess to help them decipher alien messages. You have intercepted encoded messages sent from different planets in the Andromeda Galaxy to Earth. Each intercepted message is a string containing words that correspond to specific planetary codes. Your task is to create a function `decode_message(galactic_message, codebook)` that takes in: - `galactic_message`: a string representing an encoded message. The words in the messag...

## Interaction Content
### Parsons Blocks
0. ```python
def decode_message(galactic_message, codebook):
```
1. ```python
words = galactic_message.split()
decoded_words = [''] * 0
```
2. ```python
return ' '.join(decoded_words)
```
3. ```python
for word in words:
        if word in codebook:
            decoded_words.append(codebook[word])
        else:
            decoded_words.append('UNKNOWN')
```
### Distractors
```python
decoded_words = {}
```
```python
for word in words:
        if word in codebook:
            decoded_words.extend(codebook[word])
        else:
            decoded_words.append('UNKNOWN')
```

## Answer Key
```json
{
  "solution_order": [
    0,
    1,
    3,
    2
  ],
  "ordered_blocks": [
    "def decode_message(galactic_message, codebook):",
    "words = galactic_message.split()\ndecoded_words = [''] * 0",
    "for word in words:\n        if word in codebook:\n            decoded_words.append(codebook[word])\n        else:\n            decoded_words.append('UNKNOWN')",
    "return ' '.join(decoded_words)"
  ]
}
```

## Grading Rule
Full credit only when the learner orders every displayed block exactly as in the canonical solution.

## Validation
- Passed: `True`
