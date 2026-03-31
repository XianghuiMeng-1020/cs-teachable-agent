class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("Word length exceeds grid size.")
        self.grid = [["X"] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        word_length = len(word)
        max_length = len(self.grid)
        for i in range(max_length):
            if ''.join(self.grid[i][:word_length]) == word:
                return True
            if ''.join(self.grid[j][i] for j in range(word_length)) == word:
                return True
        return False