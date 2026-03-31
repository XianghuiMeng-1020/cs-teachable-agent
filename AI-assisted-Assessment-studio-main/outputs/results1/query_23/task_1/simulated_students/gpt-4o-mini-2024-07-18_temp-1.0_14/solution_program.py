class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("All words must fit within the grid size.")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = word

    def exists(self, word: str) -> bool:
        n = len(self.grid)
        # Check horizontally
        for row in self.grid:
            if ''.join(row).find(word) != -1:
                return True
        # Check vertically
        for col in range(n):
            if ''.join(self.grid[row][col] for row in range(n)).find(word) != -1:
                return True
        return False