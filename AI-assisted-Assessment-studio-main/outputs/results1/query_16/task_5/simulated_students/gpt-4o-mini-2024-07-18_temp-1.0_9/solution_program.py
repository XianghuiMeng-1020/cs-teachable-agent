class SciFiHaiku:
    def __init__(self, text):
        self.raw_text = text

    def generate_haiku(self):
        words = self.raw_text.split()
        line1 = line2 = line3 = ''
        for word in words:
            if len(line1) < 5:
                line1 += word + ' '
            elif len(line2) < 7:
                line2 += word + ' '
            elif len(line3) < 5:
                line3 += word + ' '

        line1 = line1[:5]  # Ensure line has exactly 5 characters  
        line2 = line2[:7]  # Ensure line has exactly 7 characters  
        line3 = line3[:5]  # Ensure line has exactly 5 characters  
        return self.evaluate_expressions(line1.strip(), line2.strip(), line3.strip())

    def evaluate_expressions(self, line1, line2, line3):
        lines = [line1, line2, line3]
        evaluated_lines = []
        for line in lines:
            try:
                # Replace non-space characters with evaluated expression if it is valid
                evaluated_line = ''
                tokens = line.split()
                for token in tokens:
                    # If the token can be evaluated
                    if any(char.isdigit() for char in token):
                        result = eval(token.replace('=', '==').replace('*', 'x'))
                        evaluated_line += str(result) + ' '
                    else:
                        evaluated_line += token + ' '
                evaluated_lines.append(evaluated_line.strip()[:len(line)])
            except:
                evaluated_lines.append('Err')
        return evaluated_lines
