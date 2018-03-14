import abc


class RecommendationsSource:
    def __init__(self, source_path):
        self.source_path = source_path
        self.items = []
        self.converted_items = []
        self.sections = []
        self.books = []

    def getAllText(self):
        return open(self.source_path, 'r').read()

    # Represent items
    def representItems(self, model_converter):
        for item in self.items:
            self.converted_items.append(model_converter(item))

    def bestItems(self, model_scorer):
        return
