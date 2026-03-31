class BoardGameTournament:
    def __init__(self):
        self.participants = {}

    def add_participant(self, name):
        if name in self.participants:
            raise ValueError(f'Participant {name} already exists.')
        self.participants[name] = 0

    def record_score(self, name, score):
        if name not in self.participants:
            raise ValueError(f'Participant {name} does not exist.')
        self.participants[name] += score

    def get_score(self, name):
        if name not in self.participants:
            raise ValueError(f'Participant {name} does not exist.')
        return self.participants[name]

    def save_scores(self, filename):
        with open(filename, 'w') as f:
            for participant, score in self.participants.items():
                f.write(f'{participant}: {score}\n')

    def load_scores(self, filename):
        with open(filename, 'r') as f:
            self.participants = {}
            for line in f:
                name, score = line.strip().split(': ')
                self.participants[name] = int(score)