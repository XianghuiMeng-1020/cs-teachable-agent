class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def generate_haiku(self):
        # Splits the text into expected haiku form
        lines, line, char_count = [], '', 0
        separates = self.text.split(' ')
        for part in separates:
            while len(part) > 0:
                needed_chars = 5 if len(lines) % 2 == 0 else 7
                take = needed_chars - char_count
                if len(part) >= take:
                    line += part[:take]
                    lines.append(line)
                    line = ''
                    part = part[take:]
                    char_count = 0
                else:
                    line += part
                    char_count += len(part)
                    part = ''

        # Evaluate expressions in each line
        return self.evaluate_expressions(lines)

    def evaluate_expressions(self, lines=None):
        if lines is None:
            lines = self.text.split(' ')

        evaluated_lines = []
        for line in lines:
            try:
                if any(char.isdigit() for char in line):  # crude check for expressions
                    # Evaluate the expressions
                    eval_line = eval(line)
                    evaluated_lines.append(str(eval_line))
                else:
                    evaluated_lines.append(line)
            except Exception:
                evaluated_lines.append('Err')

        return evaluated_lines

# Test example
if __name__ == "__main__":
    haiku_input = "3+2_in_space 8-1_SN 2*2=5 where stars shine"
    haiku_instance = SciFiHaiku(haiku_input)
    haiku_output = haiku_instance.generate_haiku()
    for line in haiku_output:
        print(line)