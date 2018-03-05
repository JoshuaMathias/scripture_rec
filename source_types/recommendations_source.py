import abc


class RecommendationsSource:
    def __init__(self, sourcePath):
        self.sourcePath = sourcePath
        self.items = []
        self.sections = []
        self.books = []

    def getAllText(self):
        return open(sourcePath, 'r').read()
