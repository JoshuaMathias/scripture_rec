from nltk.tokenize import word_tokenize

# Preprocessing utilities are placed here for convenience and consistency.
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def tokenize(text):
    return word_tokenize(text)


def tokenizeStr(text):
    return " ".join(str(e) for e in word_tokenize(text))


def tokenizeTuple(text):
    tokens = word_tokenize(text)
    return tokens, " ".join(str(e) for e in tokens)
