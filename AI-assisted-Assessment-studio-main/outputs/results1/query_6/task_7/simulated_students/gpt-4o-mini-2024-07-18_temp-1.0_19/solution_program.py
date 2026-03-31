import os

class MythArchive:
    def __init__(self):
        self.archive_dir = 'myth_archive'
        os.makedirs(self.archive_dir, exist_ok=True)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            tale_name = lines[0].strip()
            tale_content = ''.join(lines[1:])
            with open(os.path.join(self.archive_dir, tale_name + '.txt'), 'w') as tale_file:
                tale_file.write(tale_content)

    def get_tale(self, name):
        try:
            with open(os.path.join(self.archive_dir, name + '.txt'), 'r') as tale_file:
                return tale_file.read()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        try:
            os.remove(os.path.join(self.archive_dir, name + '.txt'))
        except FileNotFoundError:
            pass

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.archive_dir) if f.endswith('.txt')]