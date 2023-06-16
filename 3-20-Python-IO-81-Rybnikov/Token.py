class Token():
    def __init__(self, tag, value=None):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return f"{self.tag}: {self.value}"
