class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word exceeds the allowed grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            for j in range(len(word)):
                self.grid[i][j] = word[j]

    def exists(self, word: str) -> bool:
        max_length = len(self.grid)
        # Check horizontally
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        # Check vertically
        for col in range(max_length):
            if ''.join(self.grid[row][col] for row in range(max_length)).find(word) != -1:
                return True
        return False