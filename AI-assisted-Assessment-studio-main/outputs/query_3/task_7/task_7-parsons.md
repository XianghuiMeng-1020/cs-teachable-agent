# Decoding Alien Messages

- Item ID: `task_7-parsons`
- Item Type: `parsons`
- Source Task: `task_7`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_7`

## Prompt
Rearrange the code blocks to form a function that decodes alien messages using a codebook. Words not found in the codebook should be replaced with 'UNKNOWN'. The decoded message should have words separated by a single space.

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
decoded_words = ''
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
All blocks must be in the correct order to pass.

## Validation
- Passed: `True`
