class SciFiHaiku:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def generate_haiku(self):
        words = self.raw_text.split()  
        haiku_lines = []
        current_line = ""
        line_length = [5, 7, 5]
        line_index = 0

        for word in words:
            evaluated_word = self.evaluate_expressions(word)
            if len(current_line) + len(evaluated_word) + 1 <= line_length[line_index]:
                if current_line:
                    current_line += " "
                current_line += evaluated_word
            if len(current_line) == line_length[line_index]:
                haiku_lines.append(current_line)
                current_line = ""
                line_index += 1
            if line_index >= len(line_length):
                break

        # If we have any leftover in the current line, add it
        if current_line:
            haiku_lines.append(current_line)

        return haiku_lines[:3]  

    def evaluate_expressions(self, word):
        try:
            # Replace '=' with '==' and prepare for evaluation
            if '=' in word:
                word = word.replace('=', '==')
            # Evaluate arithmetic expressions using eval()
            result = eval(word)
            return str(result)
        except:
            return "Err"