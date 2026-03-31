class WordSearch:
    def __init__(self, words: list):
        self.size = max(len(word) for word in words)
        if any(len(word) > self.size for word in words):
            raise ValueError("A word exceeds grid size.")

        self.grid = [['X'] * self.size for _ in range(self.size)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        if len(word) > self.size:
            return False
        word = list(word)
        for row in self.grid:
            if row == word:
                return True
        for col in zip(*self.grid):
            if list(col) == word:
                return True
        return False