import abc


def getRecommender(recommender_type="lda"):
    if recommender_type == "tdlm":
        from recommenders import tdlm_recommender
        return tdlm_recommender.TDLMRecommender()
    elif recommender_type == "td-idf":
        from recommenders import tdidf_recommender
        return tdidf_recommender.TDIDFRecommender()
    else: # lda
        from recommenders import lda_recommender
        return lda_recommender.LDARecommender()


class Recommender:
    # Perform the preprocessing necessary before training and testing
    @abc.abstractmethod
    def preprocess(self, text):
        NotImplementedError("Class %s doesn't implement preprocess()" % (self.__class__.__name__))

    # Trains recommendation using data at train_filename
    @abc.abstractmethod
    def train(self, train_filename):
        self.train_filename = train_filename
        # NotImplementedError("Class %s doesn't implement train()" % (self.__class__.__name__))

    # Returns the text of a recommendation
    @abc.abstractmethod
    def recommend(self, input_text):
        NotImplementedError("Class %s doesn't implement recommend()" % (self.__class__.__name__))

    # Source from which to recommend items (e.g. the Bible)
    # Expects a Bible object
    def source(self, recommendations_source):
        self.sourceCorpus = recommendations_source
