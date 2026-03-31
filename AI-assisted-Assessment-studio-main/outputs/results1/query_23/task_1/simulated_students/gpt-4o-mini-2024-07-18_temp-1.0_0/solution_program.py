class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if max_length > 26:
            raise ValueError('Word cannot be longer than the grid size.')
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            if len(word) <= max_length:
                self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        word_length = len(word)
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(len(self.grid)):
            if ''.join(self.grid[row][col] for row in range(len(self.grid))).find(word) != -1:
                return True
        return False