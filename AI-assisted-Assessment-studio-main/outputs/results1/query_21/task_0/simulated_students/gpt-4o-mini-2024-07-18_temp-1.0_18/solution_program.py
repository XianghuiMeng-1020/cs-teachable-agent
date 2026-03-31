class BoardGameTournament:
    def __init__(self):
        self.participants = {}

    def add_participant(self, name):
        if name in self.participants:
            raise ValueError('Participant already exists.')
        self.participants[name] = 0

    def record_score(self, name, score):
        if name not in self.participants:
            raise ValueError('Participant does not exist.')
        self.participants[name] += score

    def get_score(self, name):
        if name not in self.participants:
            raise ValueError('Participant does not exist.')
        return self.participants[name]

    def save_scores(self, filename):
        with open(filename, 'w') as file:
            for participant, score in self.participants.items():
                file.write(f'{participant}: {score}\n')

    def load_scores(self, filename):
        self.participants.clear()
        with open(filename, 'r') as file:
            for line in file:
                name, score = line.strip().split(': ')
                self.participants[name] = int(score)