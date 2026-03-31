class SciFiHaiku:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def generate_haiku(self):
        lines = self.raw_text.split(' ')
        haiku_lines = []
        current_line = ''
        for line in lines:
            if len(current_line) + len(line) + (1 if current_line else 0) > 7:
                haiku_lines.append(current_line)
                current_line = line
            else:
                if current_line:
                    current_line += ' ' + line
                else:
                    current_line = line
            if len(haiku_lines) == 3:
                break
        if current_line:
            haiku_lines.append(current_line)
        if len(haiku_lines) < 3:
            return None
        haiku_lines[0] = haiku_lines[0][:5]
        haiku_lines[1] = haiku_lines[1][:7]
        haiku_lines[2] = haiku_lines[2][:5]
        return [haiku_lines[0], self.evaluate_expressions(haiku_lines[1]), haiku_lines[2]]

    def evaluate_expressions(self, line):
        import re
        def eval_expression(match):
            try:
                return str(eval(match.group()))
            except:
                return 'Err'
        return re.sub(r'\d+[-+*/]\d+', eval_expression, line)
