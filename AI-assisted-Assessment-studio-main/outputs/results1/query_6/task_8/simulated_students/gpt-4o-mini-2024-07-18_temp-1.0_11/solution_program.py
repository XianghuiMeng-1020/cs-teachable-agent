class Mythology:
    def __init__(self):
        self.stories = {}
        self.read_stories_from_file('mythology_stories.txt')

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            title = None
            content = []
            for line in file:
                line = line.strip()
                if line.startswith('# Story Title:'):
                    if title is not None:
                        self.stories[title] = '\n'.join(content)
                    title = line.split(': ', 1)[1]
                    content = []
                else:
                    content.append(line)
            if title is not None:
                self.stories[title] = '\n'.join(content)

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(self.stories[title])