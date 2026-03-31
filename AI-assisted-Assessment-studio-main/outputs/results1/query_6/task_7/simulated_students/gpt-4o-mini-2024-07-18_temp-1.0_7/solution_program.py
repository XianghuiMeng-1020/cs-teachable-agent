import os

class MythArchive:
    def __init__(self):
        self.directory = 'myth_archive'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            tale_name = lines[0].strip()
            tale_content = ''.join(lines[1:])
            with open(os.path.join(self.directory, tale_name + '.txt'), 'w') as tale_file:
                tale_file.write(tale_content)

    def get_tale(self, name):
        try:
            with open(os.path.join(self.directory, name + '.txt'), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        try:
            os.remove(os.path.join(self.directory, name + '.txt'))
        except FileNotFoundError:
            pass

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.directory) if f.endswith('.txt')]