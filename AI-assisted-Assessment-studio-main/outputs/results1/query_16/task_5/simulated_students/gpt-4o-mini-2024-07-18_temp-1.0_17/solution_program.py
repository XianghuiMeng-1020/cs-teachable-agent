class SciFiHaiku:
    def __init__(self, haiku_text):
        self.haiku_text = haiku_text

    def evaluate_expressions(self, line):
        try:
            # Replace '=' with '' before evaluating to allow for simple arithmetics
            if '=' in line:
                line = line.replace('=', '')
            result = eval(line)
            return str(result)
        except:
            return 'Err'

    def generate_haiku(self):
        parts = self.haiku_text.split(' ')
        haiku_lines = []

        # Collect three lines with appropriate character counts
        line1 = line2 = line3 = ''
        for part in parts:
            if len(line1) < 5:
                line1 += part + '_'
            elif len(line2) < 7:
                line2 += part + '_'
            elif len(line3) < 5:
                line3 += part + '_'

        # Trim to exact lengths
        line1 = line1[:5]
        line2 = line2[:7]
        line3 = line3[:5]

        # Evaluate expressions
        line1 = self.evaluate_expressions(line1)
        line2 = self.evaluate_expressions(line2)
        line3 = self.evaluate_expressions(line3)

        haiku_lines.extend([line1, line2, line3])

        return '\n'.join(haiku_lines)