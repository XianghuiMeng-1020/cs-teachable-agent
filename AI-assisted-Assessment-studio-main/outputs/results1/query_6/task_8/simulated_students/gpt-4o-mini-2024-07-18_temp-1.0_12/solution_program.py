class Mythology:
    def __init__(self, filename='mythology_stories.txt'):
        self.stories = {}
        self.read_stories_from_file(filename)

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            content = file.readlines()

        title = None
        story_lines = []

        for line in content:
            if line.startswith('# Story Title:'):
                if title is not None:
                    self.stories[title] = ''.join(story_lines).strip()
                title = line[len('# Story Title:'):].strip()
                story_lines = []
            else:
                story_lines.append(line)

        if title is not None:
            self.stories[title] = ''.join(story_lines).strip()

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(self.stories[title])