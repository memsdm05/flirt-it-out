class Bot:
    def __init__(self):
        self.personalities = {}

    def read_personalities(self, path):
        with open(path) as f:
            for line in f.readlines():
                pass