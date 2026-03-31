class MythologyManager:
    def __init__(self, filename):
        self.filename = filename
        self.stories = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    name, story = line.strip().split(': ', 1)
                    self.stories[name] = story
        except FileNotFoundError:
            open(filename, 'w').close()

    def add_story(self, name, story):
        self.stories[name] = story

    def remove_story(self, name):
        if name in self.stories:
            del self.stories[name]

    def get_story(self, name):
        return self.stories.get(name, '')

    def save(self):
        with open(self.filename, 'w') as file:
            for name, story in self.stories.items():
                file.write(f'{name}: {story}\n')