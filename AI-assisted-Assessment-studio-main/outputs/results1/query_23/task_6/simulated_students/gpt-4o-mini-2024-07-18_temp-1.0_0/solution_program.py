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
        self.point_mapping = {}
        for points, letters in self.letter_points.items():
            for letter in letters:
                self.point_mapping[letter] = points

    def calculate_score(self, word):
        score = 0
        for char in word.upper():
            if char.isalpha():
                score += self.point_mapping.get(char, 0)
        return score