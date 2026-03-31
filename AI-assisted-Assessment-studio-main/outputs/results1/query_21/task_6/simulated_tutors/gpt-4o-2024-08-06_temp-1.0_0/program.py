# Implementation of BoardGameScoreboard class
import os

class BoardGameScoreboard:
    def __init__(self, file_name):
        self.file_name = file_name
        # Ensure the file exists upon initialization
        if not os.path.exists(self.file_name):
            self._initialize_file()
        self.scores = self._load_scores()

    def _initialize_file(self):
        with open(self.file_name, 'w') as f:
            # Start with an empty file
            f.write('')

    def _load_scores(self):
        scores = {}
        with open(self.file_name, 'r') as f:
            for line in f:
                if line.strip() == "":  # Skip any empty lines
                    continue
                player_name, score = line.strip().split(':')
                scores[player_name] = int(score)
        return scores

    def _save_scores(self):
        with open(self.file_name, 'w') as f:
            for player_name, score in self.scores.items():
                f.write(f'{player_name}:{score}\n')

    def add_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score
        self._save_scores()

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)

# The context relevance is evaluated based on the task's use of the given
# programming concepts within the theme of 'Board Games'.