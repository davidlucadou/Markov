class Link():
    def __init__(self, prefix: str, suffix: str):
        self.prefix = prefix
        self.suffix = suffix

    def slide(self):
        prefix_words = self.prefix.split()
        new_prefix = [prefix_words[1], self.suffix]
        self.prefix = ' '.join(new_prefix)
