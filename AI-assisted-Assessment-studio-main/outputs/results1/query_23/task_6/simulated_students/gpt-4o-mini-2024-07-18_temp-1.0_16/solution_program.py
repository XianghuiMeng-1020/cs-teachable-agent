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
        self.letter_value = {}
        for points, letters in self.letter_points.items():
            for letter in letters:
                self.letter_value[letter] = points

    def calculate_score(self, word):
        total_score = 0
        for char in word.upper():
            if char.isalpha():
                total_score += self.letter_value.get(char, 0)
        return total_score