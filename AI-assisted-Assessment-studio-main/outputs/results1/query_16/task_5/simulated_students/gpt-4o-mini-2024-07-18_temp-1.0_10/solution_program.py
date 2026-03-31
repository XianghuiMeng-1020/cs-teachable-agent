class SciFiHaiku:
    def __init__(self, text):
        self.raw_haiku = text

    def generate_haiku(self):
        lines = self.raw_haiku.split()
        result = []
        current_length = 0
        lengths = [5, 7, 5]
        index = 0

        for line in lines:
            evaluated_line = self.evaluate_expressions(line)
            if current_length + len(evaluated_line) <= lengths[index]:
                result.append(evaluated_line)
                current_length += len(evaluated_line)
            if current_length == lengths[index]:
                index += 1
                current_length = 0
            if index >= 3:
                break

        while len(result) < 3:
            result.append('')

        return '\n'.join(result)

    def evaluate_expressions(self, line):
        try:
            # Check for simple expressions 
            result = str(eval(line))
            return result
        except:
            return "Err"