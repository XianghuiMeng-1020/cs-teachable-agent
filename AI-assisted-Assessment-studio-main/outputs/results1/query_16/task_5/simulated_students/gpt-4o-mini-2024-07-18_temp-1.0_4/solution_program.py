class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def evaluate_expressions(self, expression):
        try:
            # Evaluate the mathematical expression, while  replacing any '=' with '' before evaluation
            result = eval(expression.replace('=', '=='))
            return str(result)
        except Exception:
            return 'Err'

    def generate_haiku(self):
        words = self.text.split()
        haiku_lines = [[], [], []]
        line_length = [5, 7, 5]
        current_line = 0

        for word in words:
            if len(word) > line_length[current_line]:
                continue
            haiku_lines[current_line].append(word)
            if sum(len(w) for w in haiku_lines[current_line]) + len(haiku_lines[current_line]) - 1 >= line_length[current_line]:
                current_line += 1
                if current_line >= 3:
                    break

        # Generate the final haiku
        finalized_haiku = []
        for i, line in enumerate(haiku_lines):
            line_text = ' '.join(line)
            if len(line_text) < line_length[i]:
                line_text += '_' * (line_length[i] - len(line_text))
            evaluated_line = self.evaluate_expressions(line_text)
            finalized_haiku.append(evaluated_line)

        return finalized_haiku
