class Mythology:
    def __init__(self):
        self.stories = {}
        self.read_stories_from_file('mythology_stories.txt')

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read().strip().split('\n# Story Title: ')
            for story in content:
                if story:
                    parts = story.split('\n', 1)
                    title = parts[0].strip()
                    text = parts[1].strip() if len(parts) > 1 else ''
                    self.stories[title] = text

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(f'# Story Title: {title}\n{self.stories[title]}')