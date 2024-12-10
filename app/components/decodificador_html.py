from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed)

def decode_html_entities(text):
    stripper = HTMLStripper()
    stripper.feed(text)
    return stripper.get_data()

