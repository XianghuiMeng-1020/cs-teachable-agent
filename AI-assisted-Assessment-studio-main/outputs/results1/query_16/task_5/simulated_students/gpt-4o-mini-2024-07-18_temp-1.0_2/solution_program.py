class SciFiHaiku:
    def __init__(self, text):
        self.raw_text = text
        self.haiku_lines = []

    def generate_haiku(self):
        words = self.raw_text.split()
        for word in words:
            evaluated_word = self.evaluate_expressions(word)
            self.haiku_lines.append(evaluated_word)

        self.haiku_lines = self.split_into_haiku_lines()

    def split_into_haiku_lines(self):
        first_line = []
        second_line = []
        third_line = []

        current_line = 0
        current_count = 0

        for word in self.haiku_lines:
            if current_line == 0:
                if current_count + len(word) <= 5:
                    first_line.append(word)
                    current_count += len(word)
                if current_count == 5:
                    current_line += 1
                    current_count = 0
            elif current_line == 1:
                if current_count + len(word) <= 7:
                    second_line.append(word)
                    current_count += len(word)
                if current_count == 7:
                    current_line += 1
                    current_count = 0
            elif current_line == 2:
                if current_count + len(word) <= 5:
                    third_line.append(word)
                    current_count += len(word)
                if current_count == 5:
                    break

        return [''.join(first_line), ''.join(second_line), ''.join(third_line)]

    def evaluate_expressions(self, word):
        try:
            if any(op in word for op in ['+', '-', '*', '/']):
                expression = word.replace('=', '')
                return str(eval(expression))
            else:
                return word
        except:
            return 'Err'