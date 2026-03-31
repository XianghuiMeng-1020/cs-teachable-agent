class MythologyDatabase:
    def __init__(self):
        self.database = {}

    def add_god(self, name, domain, origin):
        self.database[name] = {'domain': domain, 'origin': origin}

    def remove_god(self, name):
        if name in self.database:
            del self.database[name]

    def search_god(self, name):
        if name in self.database:
            god = self.database[name]
            return f"{name};{god['domain']};{god['origin']}"
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for name, details in self.database.items():
                f.write(f"{name};{details['domain']};{details['origin']}\n")

    def load_from_file(self, filename):
        self.database = {}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    name, domain, origin = line.strip().split(';')
                    self.add_god(name, domain, origin)
        except FileNotFoundError:
            pass
        except ValueError:
            raise ValueError('Error in file format')