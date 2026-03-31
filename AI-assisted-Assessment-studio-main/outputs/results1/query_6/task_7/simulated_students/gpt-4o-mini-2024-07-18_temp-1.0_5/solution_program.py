import os

class MythArchive:
    def __init__(self):
        self.archive_dir = 'myth_archive'
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            tale_name = file.readline().strip()
            tale_content = file.read()
        with open(os.path.join(self.archive_dir, tale_name + '.txt'), 'w') as tale_file:
            tale_file.write(tale_name + '\n' + tale_content)

    def get_tale(self, name):
        try:
            with open(os.path.join(self.archive_dir, name + '.txt'), 'r') as tale_file:
                tale_file.readline()  # Skip the first line (title)
                return tale_file.read()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        try:
            os.remove(os.path.join(self.archive_dir, name + '.txt'))
        except FileNotFoundError:
            pass

    def list_tales(self):
        return [file.replace('.txt', '') for file in os.listdir(self.archive_dir) if file.endswith('.txt')]