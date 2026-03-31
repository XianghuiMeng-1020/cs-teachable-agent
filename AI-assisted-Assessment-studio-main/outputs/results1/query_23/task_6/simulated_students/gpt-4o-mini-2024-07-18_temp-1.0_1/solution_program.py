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
        self.point_map = {letter: points for points, letters in self.letter_points.items() for letter in letters}

    def calculate_score(self, word):
        score = 0
        word = word.upper()
        for letter in word:
            if letter in self.point_map:
                score += self.point_map[letter]
        return score