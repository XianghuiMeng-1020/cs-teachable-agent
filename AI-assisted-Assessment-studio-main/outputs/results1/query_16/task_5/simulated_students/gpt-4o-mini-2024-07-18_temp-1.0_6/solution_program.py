class SciFiHaiku:
    def __init__(self, haiku_text):
        self.haiku_text = haiku_text

    def evaluate_expressions(self, line):
        try:
            # Replace simple arithmetic expressions with their results
            result = eval(line.replace('=', '=='))  # Change '=' to '==' to avoid SyntaxError
            return str(result)
        except:
            return 'Err'

    def generate_haiku(self):
        haiku_parts = self.haiku_text.split()  # Split input into parts
        haiku_lines = []
        count = 0
        current_line = ""

        for part in haiku_parts:
            if len(current_line) + len(part) + 1 <= 7 and count == 1:
                if current_line:
                    current_line += "_"
                current_line += part
            elif len(current_line) + len(part) + 1 <= 5 and count == 0:
                if current_line:
                    current_line += "_"
                current_line += part
            elif len(current_line) + len(part) + 1 <= 5 and count == 2:
                if current_line:
                    current_line += "_"
                current_line += part
            else:
                if current_line:
                    if count == 0 or count == 2:
                        haiku_lines.append(self.evaluate_expressions(current_line))
                    else:
                        haiku_lines.append(current_line)
                current_line = part
                count += 1
                if count == 3:
                    break
        if current_line:
            if count == 0 or count == 2:
                haiku_lines.append(self.evaluate_expressions(current_line))
            else:
                haiku_lines.append(current_line)

        return haiku_lines[:3]  # Ensuring we only return 3 lines