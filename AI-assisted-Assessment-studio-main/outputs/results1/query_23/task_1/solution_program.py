class WordSearch:
    def __init__(self, words):
        max_len = max(len(word) for word in words)
        if any(len(word) > max_len for word in words):
            raise ValueError("Word length exceeds grid size")
        self.size = max_len
        self.grid = [['X' for _ in range(self.size)] for _ in range(self.size)]
        for index, word in enumerate(words):
            if index < self.size: # Fill horizontally, within row index bounds
                for i, char in enumerate(word):
                    self.grid[index][i] = char
            if index < self.size: # Fill vertically, within column index bounds
                for i, char in enumerate(word):
                    self.grid[i][index] = char

    def exists(self, word):
        for row in self.grid:
            if ''.join(row).startswith(word):
                return True
        for col in range(self.size):
            column_str = ''.join(self.grid[row][col] for row in range(self.size))
            if column_str.startswith(word):
                return True
        return False
