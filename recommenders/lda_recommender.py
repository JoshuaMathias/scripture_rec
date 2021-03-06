from recommenders.recommenders import Recommender
import logging
from cleanup import preprocessing
from gensim.models.wrappers import LdaMallet
import os
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

mallet_path = '/NLP_TOOLS/tool_sets/mallet/latest/bin/mallet'


class LDARecommender(Recommender):
    def __init__(self):
        return

    def preprocess(self, text):
        return preprocessing.cleanTokens(text)

    def train(self, train_filename):
        print("train LDA")
        train_name = os.path.basename(train_filename)
        model_filename = train_name+".lda_model"
        if os.path.isfile(model_filename):
            self.model = LdaMallet.load(model_filename)
        else:
            self.corpus = preprocessing.GensimCorpus(train_filename)
            self.model = LdaMallet(mallet_path, self.corpus, num_topics=100, id2word=self.corpus.dictionary)
            self.model.save(model_filename)
            topics_str = self.model.show_topics(num_topics=-1)
            open(train_name+".lda_model.topics", 'w').write(str(topics_str))

    def recommend(self, input_text):
        input_bow = self.corpus.dictionary.doc2bow(self.preprocess(input_text))
        input_topics = self.model[input_bow]
        print("lda topics: "+str(input_topics))
        return input_text
