import os

class MythologyManager:
    def __init__(self, filename):
        self.filename = filename
        self.stories = {}
        self.load_stories()

    def load_stories(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    name, story = line.strip().split(': ', 1)
                    self.stories[name] = story

    def add_story(self, name, story):
        if name not in self.stories:
            self.stories[name] = story

    def remove_story(self, name):
        if name in self.stories:
            del self.stories[name]

    def get_story(self, name):
        return self.stories.get(name, '')

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            for name, story in self.stories.items():
                file.write(f'{name}: {story}\n')