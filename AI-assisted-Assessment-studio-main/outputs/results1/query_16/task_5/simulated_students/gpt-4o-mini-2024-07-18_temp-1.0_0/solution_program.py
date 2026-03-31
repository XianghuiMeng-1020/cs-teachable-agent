class SciFiHaiku:
    def __init__(self, text):
        self.raw_text = text

    def evaluate_expressions(self, expression):
        try:
            result = eval(expression)
            return str(result)
        except:
            return "Err"

    def generate_haiku(self):
        words = self.raw_text.split(" ")
        haiku_lines = []
        current_line = ""
        char_counts = [5, 7, 5]
        current_line_index = 0

        for word in words:
            if len(current_line) + len(word) + 1 <= char_counts[current_line_index]:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                if current_line:
                    haiku_lines.append(current_line)
                if current_line_index < 2:
                    current_line_index += 1
                    current_line = word
                else:
                    haiku_lines.append(word)
                    break
            if len(current_line) == char_counts[current_line_index]:
                haiku_lines.append(current_line)
                current_line_index += 1
                current_line = ""

        # Add remaining line if not added
        if current_line:  
            haiku_lines.append(current_line)

        # Evaluate haiku lines
        evaluated_haiku = []
        for line in haiku_lines:
            evaluated_line = ""
            for part in line.split():
                if any(char.isdigit() for char in part) and any(op in part for op in ['+', '-', '*', '/']):
                    evaluated_line += self.evaluate_expressions(part) + " "
                else:
                    evaluated_line += part + " "
            evaluated_haiku.append(evaluated_line.strip())

        return evaluated_haiku