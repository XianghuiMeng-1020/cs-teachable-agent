class WordSearch:
    def __init__(self, words: list):
        if not words:
            self.grid = []
            return
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("Words cannot be longer than grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for index, word in enumerate(words):
            self.grid[index][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        grid_size = len(self.grid)
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(grid_size):
            if ''.join(self.grid[row][col] for row in range(grid_size)).find(word) != -1:
                return True
        return False