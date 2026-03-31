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
        self.score_map = self.create_score_map() 

    def create_score_map(self):
        score_map = {}
        for score, letters in self.letter_points.items():
            for letter in letters:
                score_map[letter] = score
        return score_map

    def calculate_score(self, word):
        total_score = 0
        for char in word.upper():
            if char.isalpha():
                total_score += self.score_map.get(char, 0)
        return total_score