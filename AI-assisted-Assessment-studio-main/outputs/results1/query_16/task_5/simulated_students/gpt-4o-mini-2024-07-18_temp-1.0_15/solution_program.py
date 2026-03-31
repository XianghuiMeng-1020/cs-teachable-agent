class SciFiHaiku:
    def __init__(self, haiku_text):
        self.haiku_text = haiku_text

    def generate_haiku(self):
        words = self.haiku_text.split()  
        line1, line2, line3 = [], [], []
        char_count = 0

        # Distributing words into lines based on character lengths
        for word in words:
            evaluated_word = self.evaluate_expressions(word)
            char_count += len(evaluated_word)
            if 0 <= len(line1) < 5 and char_count <= 5:
                line1.append(evaluated_word)
            elif 0 <= len(line2) < 7 and char_count <= (5 + 7):
                line2.append(evaluated_word)
            elif 0 <= len(line3) < 5 and char_count <= (5 + 7 + 5):
                line3.append(evaluated_word)

        # Joining lines then ensuring length requirements
        line1_str = ''.join(line1)[:5].ljust(5)
        line2_str = ''.join(line2)[:7].ljust(7)
        line3_str = ''.join(line3)[:5].ljust(5)

        # Printing final haiku
        print(line1_str)
        print(line2_str)
        print(line3_str)

    def evaluate_expressions(self, expression):
        try:
            result = eval(expression.replace('=', '==').replace('*', 'x'))
            return str(result)
        except:
            return 'Err'