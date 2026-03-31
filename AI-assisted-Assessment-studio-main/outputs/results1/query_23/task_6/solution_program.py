class ScrabbleScoreCalculator:
    def __init__(self):
        self.letter_points = {
            1: "AEIOULNRST",
            2: "DG",
            3: "BCMP",
            4: "FHVWY",
            5: "K",
            8: "JX",
            10: "QZ"
        }

    def calculate_score(self, word):
        total_score = 0
        word = word.upper()
        for char in word:
            for points, letters in self.letter_points.items():
                if char in letters:
                    total_score += points
                    break
        return total_score
