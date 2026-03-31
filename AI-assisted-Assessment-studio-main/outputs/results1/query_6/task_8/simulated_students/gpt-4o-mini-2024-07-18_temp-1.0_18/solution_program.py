class Mythology:
    def __init__(self):
        self.stories = {}
        self.read_stories_from_file('mythology_stories.txt')

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            current_title = None
            current_story = []
            
            for line in file:
                line = line.strip()
                if line.startswith('# Story Title:'):
                    if current_title:
                        self.stories[current_title] = '\n'.join(current_story)
                    current_title = line[len('# Story Title: '):]
                    current_story = []
                else:
                    current_story.append(line)
            
            if current_title:
                self.stories[current_title] = '\n'.join(current_story)

    def get_story(self, titles):
        return [self.stories[title] for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(self.stories[title])