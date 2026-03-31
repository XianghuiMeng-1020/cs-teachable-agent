class SciFiHaiku:
    def __init__(self, haiku_text):
        self.haiku_text = haiku_text

    def generate_haiku(self):
        raw_lines = self.haiku_text.split(' ')
        lines = []
        current_line = ''

        for raw in raw_lines:
            evaluated = self.evaluate_expressions(raw)
            if len(current_line) + len(evaluated) <= 7:
                current_line += evaluated + ' '
            else:
                if len(current_line.strip()) == 5:
                    lines.append(current_line.strip())
                    current_line = evaluated + ' '
                else:
                    current_line += evaluated + ' '
            if len(current_line) >= 7:
                lines.append(current_line.strip())
                current_line = ''

        if current_line.strip():
            lines.append(current_line.strip())

        while len(lines) < 3:
            lines.append('')

        if len(lines[0]) < 5:
            lines[0] = lines[0].ljust(5)[:5]  
        if len(lines[1]) < 7:
            lines[1] = lines[1].ljust(7)[:7]  
        if len(lines[2]) < 5:
            lines[2] = lines[2].ljust(5)[:5]  

        return '\n'.join(lines)

    def evaluate_expressions(self, expression):
        try:
            if '=' in expression:
                expression = expression.split('=')[0]
            result = eval(expression)
            return str(result)
        except:
            return 'Err'