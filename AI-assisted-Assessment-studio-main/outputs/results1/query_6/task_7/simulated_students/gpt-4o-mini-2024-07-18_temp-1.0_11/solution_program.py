import os

class MythArchive:
    def __init__(self):
        self.archive_dir = 'myth_archive'
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def add_tale(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if not lines:
                return
            tale_name = lines[0].strip()
            tale_content = ''.join(lines[1:]).strip()
            with open(os.path.join(self.archive_dir, tale_name + '.txt'), 'w') as tale_file:
                tale_file.write(tale_content)

    def get_tale(self, name):
        file_path = os.path.join(self.archive_dir, name + '.txt')
        if not os.path.exists(file_path):
            return ''
        with open(file_path, 'r') as f:
            return f.read()

    def remove_tale(self, name):
        file_path = os.path.join(self.archive_dir, name + '.txt')
        if os.path.exists(file_path):
            os.remove(file_path)

    def list_tales(self):
        return [file.replace('.txt', '') for file in os.listdir(self.archive_dir) if file.endswith('.txt')]