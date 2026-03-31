class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def evaluate_expressions(self, line):
        try:
            # Replace the expressions with their results
            parts = line.split()  # Split the line into words/expressions
            for i, part in enumerate(parts):
                # Check for valid mathematical expression by evaluating it
                if any(op in part for op in '+-*/'):  # Simplified check for expressions
                    result = eval(part)
                    parts[i] = str(result)  # Replace with result if valid
            return ' '.join(parts)
        except:
            return "Err"  # In case of any error, return 'Err'

    def generate_haiku(self):
        lines = self.text.split('\n')
        haiku = []
        for line in lines:
            # Evaluate expressions in each line and save to haiku
            evaluated_line = self.evaluate_expressions(line)
            haiku.append(evaluated_line)

        # Ensure the haiku follows the 5-7-5 structure
        haiku_lines = [self._format_line(haiku[0][:5]),
                       self._format_line(haiku[1][:7]),
                       self._format_line(haiku[2][:5])]
        return '\n'.join(haiku_lines)

    def _format_line(self, line):
        return line.ljust(5)[:5]  # Ensure the line has exactly 5 characters by trimming or padding

# This code defines the SciFiHaiku class that will be able to create Sci-Fi haikus according to the specified requirements.