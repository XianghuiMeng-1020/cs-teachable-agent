import os

class MythArchive:
    def __init__(self):
        self.archive_dir = 'myth_archive'
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            tale_name = lines[0].strip()
            tale_content = ''.join(lines[1:])
            with open(os.path.join(self.archive_dir, tale_name + '.txt'), 'w') as tale_file:
                tale_file.write(tale_content)

    def get_tale(self, name):
        tale_path = os.path.join(self.archive_dir, name + '.txt')
        if not os.path.isfile(tale_path):
            return ''
        with open(tale_path, 'r') as tale_file:
            return tale_file.read()

    def remove_tale(self, name):
        tale_path = os.path.join(self.archive_dir, name + '.txt')
        if os.path.isfile(tale_path):
            os.remove(tale_path)

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.archive_dir) if f.endswith('.txt')]
