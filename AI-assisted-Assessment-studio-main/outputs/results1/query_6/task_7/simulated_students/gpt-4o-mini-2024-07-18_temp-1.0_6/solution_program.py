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
            tale_file.write(tale_content)

    def get_tale(self, name):
        file_path = os.path.join(self.archive_dir, name + '.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r') as tale_file:
                return tale_file.read()
        return ''

    def remove_tale(self, name):
        file_path = os.path.join(self.archive_dir, name + '.txt')
        if os.path.exists(file_path):
            os.remove(file_path)

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.archive_dir) if f.endswith('.txt')]