import os

class MythArchive:
    def __init__(self):
        self.archive_dir = 'myth_archive'
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def add_tale(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if lines:
                tale_name = lines[0].strip()
                tale_content = ''.join(lines[1:])
                with open(os.path.join(self.archive_dir, tale_name + '.txt'), 'w') as tale_file:
                    tale_file.write(tale_content)

    def get_tale(self, name):
        file_name = os.path.join(self.archive_dir, name + '.txt')
        if os.path.isfile(file_name):
            with open(file_name, 'r') as tale_file:
                return tale_file.read()
        return ''

    def remove_tale(self, name):
        file_name = os.path.join(self.archive_dir, name + '.txt')
        if os.path.isfile(file_name):
            os.remove(file_name)

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.archive_dir) if f.endswith('.txt')]
