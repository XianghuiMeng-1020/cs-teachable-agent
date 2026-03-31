class SciFiHaiku:
    def __init__(self, text):
        self.raw_text = text

    def generate_haiku(self):
        lines = self.raw_text.split()
        haiku = [self.evaluate_expressions(line) for line in lines]

        haiku_lines = []
        temp = ''

        for line in haiku:
            if len(temp) + len(line) < 5:
                temp += line + ' '
            elif len(temp) + len(line) >= 5:
                haiku_lines.append(temp[:5])
                temp = line
                if len(temp) == 5:
                    haiku_lines.append(temp)
                    temp = ''
            if len(haiku_lines) == 3:
                break

        if temp:
            haiku_lines.append(temp)

        # Now ensure we have 3 lines total
        while len(haiku_lines) < 3:
            haiku_lines.append('')

        # Ensure second line has exact 7 length
        if len(haiku_lines[1]) < 7:
            haiku_lines[1] += ' ' * (7 - len(haiku_lines[1]))

        return haiku_lines

    def evaluate_expressions(self, line):
        try:
            # Replace all spaces with '' for evaluation
            result = eval(line.replace('_',''))
            return str(result)
        except:
            return 'Err'
