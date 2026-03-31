class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("One or more words are longer than the grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            if i < max_length:
                self.grid[i][:len(word)] = word

    def exists(self, word: str) -> bool:
        grid_size = len(self.grid)
        # check horizontally
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        # check vertically
        for col in range(grid_size):
            vertical_word = ''.join(self.grid[row][col] for row in range(grid_size))
            if vertical_word.find(word) != -1:
                return True
        return False