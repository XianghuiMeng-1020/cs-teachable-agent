import os

class MythArchive:
    def __init__(self):
        self.directory = 'myth_archive'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            name = file.readline().strip()
            content = file.read()
        with open(os.path.join(self.directory, name + '.txt'), 'w') as archive_file:
            archive_file.write(content)

    def get_tale(self, name):
        try:
            with open(os.path.join(self.directory, name + '.txt'), 'r') as archive_file:
                return archive_file.read()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        try:
            os.remove(os.path.join(self.directory, name + '.txt'))
        except FileNotFoundError:
            pass

    def list_tales(self):
        return [f[:-4] for f in os.listdir(self.directory) if f.endswith('.txt')]