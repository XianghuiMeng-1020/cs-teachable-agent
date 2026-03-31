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
        self.point_values = {}
        for points, letters in self.letter_points.items():
            for letter in letters:
                self.point_values[letter] = points

    def calculate_score(self, word):
        total_score = 0
        word = word.upper()
        for char in word:
            if char in self.point_values:
                total_score += self.point_values[char]
        return total_score