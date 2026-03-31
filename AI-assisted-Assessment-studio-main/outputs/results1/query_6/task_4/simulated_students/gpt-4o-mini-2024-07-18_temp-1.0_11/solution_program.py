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
            god_info = self.database[name]
            return f"{name};{god_info['domain']};{god_info['origin']}"
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for name, info in self.database.items():
                f.write(f"{name};{info['domain']};{info['origin']}\n")

    def load_from_file(self, filename):
        self.database.clear()
        try:
            with open(filename, 'r') as f:
                for line in f:
                    name, domain, origin = line.strip().split(';')
                    self.add_god(name, domain, origin)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading file: {e}")