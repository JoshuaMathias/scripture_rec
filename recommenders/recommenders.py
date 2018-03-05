import abc


def recommender(recommenderType="lda"):
    if recommenderType == "tdlm":
        import tdlm_recommender
        return tdlm_recommender.TDLMRecommender()
    elif recommenderType == "td-idf":
        import tdidf_recommender
        return tdidf_recommender.TDIDFRecommender()
    else: # lda
        import lda_recommender
        return lda_recommender.LDARecommender()


class Recommender:
    # @abc.abstractmethod
    # def __init__(self, method):
    #     self.method = method

    @abc.abstractmethod
    def recommend(self, inputText):
        NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

    # Source from which to recommend items (e.g. the Bible)
    # Expects a Bible object
    def source(self, recommendationsSource):
        self.sourceCorpus = recommendationsSource
