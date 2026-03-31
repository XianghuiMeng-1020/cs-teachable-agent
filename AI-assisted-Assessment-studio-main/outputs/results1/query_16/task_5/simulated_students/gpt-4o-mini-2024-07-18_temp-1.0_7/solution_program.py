class SciFiHaiku:
    def __init__(self, haiku_text):
        self.haiku_text = haiku_text

    def evaluate_expressions(self, line):
        import re
        def eval_expression(match):
            try:
                # Replace '=' with '==' for evaluation using eval
                expression = match.group(0).replace('=', '==')
                result = eval(expression)
                return str(result)
            except:
                return 'Err'

        # Find all expressions and evaluate them
        return re.sub(r'\d+[+\-*/]\d+=?\d*', eval_expression, line)

    def generate_haiku(self):
        words = self.haiku_text.split()
        if len(words) < 3:
            return []

        haiku = []
        for word in words:
            if len(haiku) < 2 and len(word) <= 7:
                haiku.append(word)
            elif len(haiku) < 3 and len(word) <= 5:
                haiku.append(word)
            if len(haiku) == 3:
                break

        # Adjusting lines to 5-7-5 exactly
        formatted_haiku = [self.evaluate_expressions(haiku[0][:5]),
                            self.evaluate_expressions(haiku[1][:7]),
                            self.evaluate_expressions(haiku[2][:5])]
        return formatted_haiku