class Mythology:
    def __init__(self, filename='mythology_stories.txt'):
        self.stories = {}
        self.read_stories_from_file(filename)

    def read_stories_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            current_title = None
            current_content = []
            for line in lines:
                line = line.strip()
                if line.startswith('# Story Title:'):
                    if current_title:
                        # Save the previous story
                        self.stories[current_title] = ' '.join(current_content)
                    # Start a new story
                    current_title = line.replace('# Story Title: ', '')
                    current_content = []
                else:
                    current_content.append(line)
            # Save the last story in the file
            if current_title:
                self.stories[current_title] = ' '.join(current_content)

    def get_story(self, titles):
        return [self.stories.get(title, '') for title in titles if title in self.stories]

    def save_story_to_file(self, title, filename):
        if title in self.stories:
            with open(filename, 'w') as file:
                file.write(self.stories[title])