class Mythology:
    def __init__(self):
        self.stories = {}
        self.read_stories_from_file('mythology_stories.txt')

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            story_title = None
            story_content = []
            for line in file:
                line = line.strip()
                if line.startswith('# Story Title:'):
                    if story_title:
                        self.stories[story_title] = '\n'.join(story_content)
                    story_title = line[15:]  # Extract title after '# Story Title:'
                    story_content = []
                elif story_title:
                    story_content.append(line)
            if story_title:
                self.stories[story_title] = '\n'.join(story_content)  # Save the last story

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(f'# Story Title: {title}\n{self.stories[title]}')