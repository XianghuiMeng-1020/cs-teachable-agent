class SciFiHaiku:
    def __init__(self, text):
        self.text = text

    def evaluate_expressions(self, line):
        try:
            # Replace special characters for evaluation
            expr = line.replace("=", "==").replace("*", "*")
            result = eval(expr)
            return str(result)
        except:
            return "Err"

    def generate_haiku(self):
        words = self.text.split()
        haiku_lines = []
        line_lengths = [5, 7, 5]

        current_line = ""

        for word in words:
            expr_result = self.evaluate_expressions(word)
            determined_length = len(expr_result) if "Err" not in expr_result else len(word)

            if len(current_line) + determined_length <= line_lengths[len(haiku_lines)]:
                if current_line:
                    current_line += " "
                current_line += expr_result
            else:
                haiku_lines.append(current_line)
                current_line = expr_result

            if len(haiku_lines) == 3:
                break

        haiku_lines.append(current_line)

        return [line.ljust(length)[:length] for line, length in zip(haiku_lines, line_lengths)]

# Example usage
# haiku = SciFiHaiku("3+2_in_space 8-1_SN 2*2=5 where stars shine")
# generated_haiku = haiku.generate_haiku()
# for line in generated_haiku:
#     print(line)