class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word is longer than the maximum grid size.")
        self.grid_size = max_length
        self.grid = [['X'] * self.grid_size for _ in range(self.grid_size)]
        for i, word in enumerate(words):
            self.grid[i][0:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        word_length = len(word)  
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        for col in range(self.grid_size):
            if ''.join(self.grid[row][col] for row in range(self.grid_size)).find(word) != -1:
                return True
        return False