class WordSearch:
    def __init__(self, words: list):
        if not words:
            self.grid = []
            return
        max_length = max(len(word) for word in words)
        if max_length > 26:
            raise ValueError("A word cannot be longer than 26 characters.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            if len(word) > max_length:
                raise ValueError("A word cannot be longer than the grid size.")
            for j, char in enumerate(word):
                self.grid[i][j] = char

    def exists(self, word: str) -> bool:
        grid_size = len(self.grid)
        for i in range(grid_size):
            # Check horizontally
            if ''.join(self.grid[i]).find(word) != -1:
                return True
            # Check vertically
            vertical_word = ''.join(self.grid[j][i] for j in range(grid_size))
            if vertical_word.find(word) != -1:
                return True
        return False