class ScrabbleScoreCalculator:
    def __init__(self):
        self.letter_points = {
            1: ['A', 'E', 'I', 'O', 'U', 'L', 'N', 'R', 'S', 'T'],
            2: ['D', 'G'],
            3: ['B', 'C', 'M', 'P'],
            4: ['F', 'H', 'V', 'W', 'Y'],
            5: ['K'],
            8: ['J', 'X'],
            10: ['Q', 'Z']
        }

    def calculate_score(self, word):
        word = word.upper()
        score = 0
        for char in word:
            for points, letters in self.letter_points.items():
                if char in letters:
                    score += points
                    break
        return score

# Test case execution is omitted here since it involves external test cases and framework requirements.