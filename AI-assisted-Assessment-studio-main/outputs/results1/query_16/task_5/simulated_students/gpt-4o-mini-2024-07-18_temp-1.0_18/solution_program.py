class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def generate_haiku(self):
        words = self.text.split()
        lines = []
        for word in words:
            evaluated = self.evaluate_expressions(word)
            if len(lines) < 2:
                if len(lines) == 0 and len(evaluated) <= 5:
                    lines.append(evaluated)
                elif len(lines) == 1 and len(evaluated) <= 7:
                    lines.append(evaluated)
                elif len(lines) == 1 and len(evaluated) <= 5:
                    lines.append(evaluated)

        # Fill first and last line with 5 char long expressions
        while len(lines[0]) < 5:
            lines[0] += '_'
        while len(lines[1]) < 7:
            if lines[1].count(' ') == 0:
                lines[1] += ' '
            else:
                lines[1] += '_'
        while len(lines[2]) < 5:
            lines[2] += '_'

        return lines

    def evaluate_expressions(self, word):
        try:
            # Replace = with == for eval compatibility
            if '=' in word:
                expression = word.replace('=', '==')
                if eval(expression):
                    return str(eval(expression))
                else:
                    return "Err"
            else:
                return str(eval(word))
        except:
            return "Err"