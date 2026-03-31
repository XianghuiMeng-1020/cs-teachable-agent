class SciFiHaiku:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def evaluate_expressions(self, text):
        result = []
        elements = text.split()  # Split on whitespace
        for element in elements:
            try:
                # Evaluate if it is a valid expression
                evaluated_value = eval(element.replace('=', '=='))  # Change assignment to comparison to evaluate
                result.append(str(int(evaluated_value)))
            except:
                result.append("Err")  # Handle errors gracefully
        return ' '.join(result)

    def generate_haiku(self):
        words = self.raw_text.split('\n')
        haiku_lines = []
        count = 0

        for word in words:
            if count == 0:  # First line should have 5 char
                if len(word) >= 5:
                    haiku_lines.append(word[:5])
                else:
                    haiku_lines.append(word.ljust(5))
                count += 1
            elif count == 1:  # Second line should have 7 char
                if len(word) >= 7:
                    haiku_lines.append(word[:7])
                else:
                    haiku_lines.append(word.ljust(7))
                count += 1
            elif count == 2:  # Third line should have 5 char
                if len(word) >= 5:
                    haiku_lines.append(word[:5])
                else:
                    haiku_lines.append(word.ljust(5))
                break  # No need for more lines

        evaluated_haiku = [self.evaluate_expressions(line) for line in haiku_lines]
        return (evaluated_haiku[0], evaluated_haiku[1], evaluated_haiku[2])

# To test the implementation you would create an instance of SciFiHaiku and call the generate_haiku method.