from nltk.tokenize import word_tokenize

# Preprocessing utilities are placed here for convenience and consistency.
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import os
from gensim import corpora, utils

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def iter_documents(given_dir):
    """Iterate over documents, yielding one document at a time."""
    if os.path.isdir(given_dir):
        for fname in os.listdir(given_dir):
            # read each document as one big string
            document = open(os.path.join(given_dir, fname)).read()
            document = cleanTokens(document)
            # parse document into a list of utf8 tokens
            # yield utils.simple_preprocess(document)
            yield document
    else:
        document = open(given_dir).read()
        yield utils.simple_preprocess(document)


class GensimCorpus(object):
    def __init__(self, corpus_dir):
        self.corpus_dir = corpus_dir
        # Given a list of tokens, return a gensim dictionary of unique tokens
        # Only includes tokens that appear more than 5 times and less than 50% of the corpus.
        self.dictionary = corpora.Dictionary(iter_documents(corpus_dir))
        self.dictionary.filter_extremes(no_below=1, no_above=1)  # remove stopwords etc

    def __iter__(self):
        for tokens in iter_documents(self.corpus_dir):
            yield self.dictionary.doc2bow(tokens)


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def cleanTokens(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalizedTokens = [lemma.lemmatize(word) for word in punc_free.split()]
    return normalizedTokens



def tokenize(text):
    return word_tokenize(text)


def tokenizeStr(text):
    return " ".join(str(e) for e in word_tokenize(text))


def tokenizeTuple(text):
    tokens = word_tokenize(text)
    return tokens, " ".join(str(e) for e in tokens)
