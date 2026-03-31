class WordSearch:
    def __init__(self, words: list):
        if not words:
            self.grid = []
            return
        max_length = max(len(word) for word in words)
        for word in words:
            if len(word) > max_length:
                raise ValueError("A word is longer than the grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        grid_size = len(self.grid)
        word_length = len(word)
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(grid_size):
            column_string = ''.join(self.grid[row][col] for row in range(grid_size))
            if column_string.find(word) != -1:
                return True
        return False