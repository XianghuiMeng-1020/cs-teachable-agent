class SciFiHaiku:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def generate_haiku(self):
        # Split the raw text into words
        words = self.raw_text.split()
        haiku = []
        # Attempt to create lines of haiku based on character count
        for word in words:
            # Evaluate the expression and replace with result or 'Err'
            evaluated_word = self.evaluate_expressions(word)
            haiku.append(evaluated_word)
            if len(haiku[0]) == 5 and len(haiku[1]) == 7 and len(haiku[2]) == 5:
                break
        # Regenerate the haiku lines to ensure they are valid
        # The first line must have 5 characters
        line1 = haiku[0][:5] + ('_' * (5-len(haiku[0])))
        # The second line must have 7 characters
        line2 = haiku[1]+ ('_' * (7-len(haiku[1])))
        # The third line must have 5 characters
        line3 = haiku[2][:5] + ('_' * (5-len(haiku[2])))
        return line1, line2, line3

    def evaluate_expressions(self, word):
        try:
            # Replace '=' with '==' for evaluation
            clean_word = word.replace('=', '==')
            if ('+' in clean_word) or ('-' in clean_word) or ('*' in clean_word) or ('/' in clean_word):
                result = eval(clean_word)
                return str(result)
            return word
        except:
            return 'Err'