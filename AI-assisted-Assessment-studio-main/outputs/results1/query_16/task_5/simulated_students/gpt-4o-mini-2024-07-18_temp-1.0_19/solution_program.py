class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def generate_haiku(self):
        words = self.text.split()  
        lines = []
        line_length = [5, 7, 5]
        current_line = 0 
        current_count = 0
        current_line_text = ''

        for word in words:
            evaluated_word = self.evaluate_expressions(word)
            if current_count + len(evaluated_word) > line_length[current_line]:
                lines.append(current_line_text)
                current_line += 1
                current_count = 0
                current_line_text = ''
                if current_line >= 3:
                    break
            if current_count > 0:
                current_line_text += ' '
                current_count += 1
            current_line_text += evaluated_word
            current_count += len(evaluated_word)

        # Add last line if not already added
        if current_line_text and current_line < 3:
            lines.append(current_line_text)

        # If we have less than 3 lines, we need to pad them to ensure we adhere to the format
        while len(lines) < 3:
            lines.append(' ' * line_length[len(lines)])

        return '\n'.join(lines)

    def evaluate_expressions(self, expression):
        try:
            # Replace = with equality checking, since we don't use it in output
            result = eval(expression.replace('=', '==').replace(' ', ''))
            if isinstance(result, (int, float)):
                return str(result)
            return expression
        except:
            return 'Err'