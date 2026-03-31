class WordSearch:
    def __init__(self, words: list):
        if not words:
            self.grid = []
            return
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word is longer than the maximum allowed length.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            for j in range(len(word)):
                self.grid[i][j] = word[j]

    def exists(self, word: str) -> bool:
        length = len(word)
        if length > len(self.grid):
            return False
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(len(self.grid)):
            if ''.join(self.grid[row][col] for row in range(len(self.grid))).find(word) != -1:
                return True
        return False