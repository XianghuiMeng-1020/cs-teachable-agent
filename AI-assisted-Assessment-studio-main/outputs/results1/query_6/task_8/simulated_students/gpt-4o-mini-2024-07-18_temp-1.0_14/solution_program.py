class Mythology:
    def __init__(self, filename='mythology_stories.txt'):
        self.stories = {}
        self.read_stories_from_file(filename)

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            current_title = None
            current_content = []
            for line in file:
                line = line.strip()
                if line.startswith('# Story Title:'):
                    if current_title is not None:
                        self.stories[current_title] = '\n'.join(current_content)
                    current_title = line[len('# Story Title: '):].strip()
                    current_content = []
                else:
                    current_content.append(line)
            if current_title is not None:
                self.stories[current_title] = '\n'.join(current_content)

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(self.stories[title])