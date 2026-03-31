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
        self.points_map = self._create_points_map()

    def _create_points_map(self):
        points_map = {}
        for points, letters in self.letter_points.items():
            for letter in letters:
                points_map[letter] = points
        return points_map

    def calculate_score(self, word):
        score = 0
        word = word.upper()
        for char in word:
            if char in self.points_map:
                score += self.points_map[char]
        return score
