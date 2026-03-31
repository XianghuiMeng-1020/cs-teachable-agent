class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def generate_haiku(self):
        lines = self.text.split(' ')
        haiku_lines = [lines[i] for i in range(min(len(lines), 3))]
        haiku_lines[0] = haiku_lines[0][:5]
        haiku_lines[1] = haiku_lines[1][:7]
        haiku_lines[2] = haiku_lines[2][:5]
        evaluated_haiku = self.evaluate_expressions(haiku_lines)
        return evaluated_haiku

    def evaluate_expressions(self, lines):
        results = []
        for line in lines:
            try:
                if any(char in line for char in ['+', '-', '*', '/']):
                    result = str(eval(line.replace('=', '==')))
                else:
                    result = line
                results.append(result)
            except:
                results.append('Err')
        return results