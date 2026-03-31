class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def generate_haiku(self):
        lines = self._split_haiku(self.text)
        evaluated_lines = []
        for line in lines:
            evaluated_lines.extend(self._evaluate_line(line))
        return evaluated_lines

    def _split_haiku(self, text):
        segments = text.split()
        lines = []
        for seg in segments:
            lines.append(seg)
            if len(seg) % 5 == 0:
                lines.append(seg)
        return lines

    def _evaluate_line(self, line):
        evaluated = []
        try:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                evaluated.append(str(eval(line)))
            else:
                evaluated.append(line)
        except:
            evaluated.append('Err')
        return evaluated

    def evaluate_expressions(self):
        return [self._evaluate_line(segment)[0] for segment in self.text.split()]