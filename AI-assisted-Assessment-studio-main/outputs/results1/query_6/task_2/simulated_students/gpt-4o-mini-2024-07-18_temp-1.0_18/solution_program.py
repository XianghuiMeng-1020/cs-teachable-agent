import os

class MythologyManager:
    def __init__(self, filename):
        self.filename = filename
        self.stories = {}
        if os.path.exists(filename):
            self.load() 

    def add_story(self, name, story):
        if name not in self.stories:
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

    def load(self):
        with open(self.filename, 'r') as file:
            for line in file:
                if ': ' in line:
                    name, story = line.split(': ', 1)
                    self.stories[name] = story.strip()