class WordSearch:
    def __init__(self, words: list):
        if not words:
            self.grid = []
            return
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word is longer than the grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        max_length = len(self.grid)
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(max_length):
            if ''.join(self.grid[row][col] for row in range(max_length)).find(word) != -1:
                return True
        return False