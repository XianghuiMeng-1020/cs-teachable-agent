class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word exceeds the maximum grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        word_length = len(word)
        grid_size = len(self.grid)
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(grid_size):
            column_string = ''.join(self.grid[row][col] for row in range(grid_size))
            if column_string.find(word) != -1:
                return True
        return False