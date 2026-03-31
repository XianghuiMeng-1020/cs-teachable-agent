class WordSearch:
    def __init__(self, words: list):
        max_length = max(len(word) for word in words)
        if any(len(word) > max_length for word in words):
            raise ValueError("A word is longer than the grid size")
        self.grid = [['X'] * max_length for _ in range(max_length)]
        for i, word in enumerate(words):
            if i < max_length:
                self.grid[i][:len(word)] = list(word)

    def exists(self, word: str) -> bool:
        max_length = len(self.grid)
        word_length = len(word)
        if word_length > max_length:
            return False
        word_list = [''.join(self.grid[i]) for i in range(max_length)]
        for j in range(max_length):
            word_list.append(''.join(self.grid[i][j] for i in range(max_length)))
        return word in word_list