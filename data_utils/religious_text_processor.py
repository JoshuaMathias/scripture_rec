# %%writefile scripture_rec/data_utils/religious_text_processor.py
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import regex as re
from collections import defaultdict
nltk.download('stopwords')
nltk.download('punkt')

# Class for preprocessing, preparing of text in the 
#   religious domain; e.g. scriptures, religious speeches
class ReligiousTextProcessor:
  # If bow, do clean_bow on __call__
  def __init__(self, bow=False):
    self.bow = bow
    self.expand = set(['—','–','-','.','/'])
    self.stemmer = PorterStemmer()
    self.stop_words = set(stopwords.words('english'))
    self.stop_words |= set(['com', 'edu', 'org', 'net', ':'])
    self.clean_vocab = defaultdict(int)
    self.bow_vocab = defaultdict(int)
    self.clean_vocab_indices = {}
    self.bow_vocab_indices = {}
    self.exclude = set(string.punctuation)
    self.exclude |= set(['—','–','-'])
    # Only keep ASCII letters, number, and colons that are between other chars (scripture references)
    self.remove_pattern = re.compile(r'[^\p{L}\p{N}:\s]|\s:\s')
    self.wordnum_pattern = re.compile(r'(\p{L})(\p{N})|(\p{N})(\p{L})')
    self.wordnum_replace = r'\1\3 \2\4'
    self.extra_space_pattern = re.compile(r' {2,}')
    self.punc_trans = str.maketrans(dict.fromkeys(self.exclude, ' '))

  # Reinitialize vocab
  def restart(self):
    self.clean_vocab = defaultdict(int)
    self.bow_vocab = defaultdict(int)

  # Return clean text
  # sent_tokenize, word_tokenize, lowercase, stem, remove stops
  def clean(self, text, do_stem=True):
    processed_text = ""

    for ch in text:
      if ch in self.expand:
        processed_text += " "+ch+" "
      else:
        processed_text += ch.lower()
    cleaned_text = ""
    # Put space between numbers and letters
    processed_text = re.sub(self.wordnum_pattern, self.wordnum_replace, processed_text)
    for sentence in sent_tokenize(processed_text):
      for word in word_tokenize(sentence):
        if word and word not in self.stop_words:
          if do_stem:
            word = self.stemmer.stem(word)
          cleaned_text += " "+word
    return cleaned_text.strip()

  def tokenize(self, text):
    processed_text = ""

    for ch in text:
      if ch in self.expand:
        processed_text += " "+ch+" "
      else:
        processed_text += ch.lower()
    cleaned_text = ""
    # Put space between numbers and letters
    processed_text = re.sub(self.wordnum_pattern, self.wordnum_replace, processed_text)
    for sentence in sent_tokenize(processed_text):
      for word in word_tokenize(sentence):
        cleaned_text += " "+word
    return cleaned_text.strip().split()

  # Given a list of texts, return a list of sentences represented as lists of words
  # Also return a dict of vocab indices
  def tokenize_vocab(self, texts):
    vocab = {}
    cleaned_texts = []
    for text in texts:
      tokens = self.tokenize(text)
      cleaned_texts.append(tokens)
      for token in tokens:
        if token not in vocab:
          vocab[token] = len(vocab)
    lprint(vocab, 'precleaned vocab')
    return cleaned_texts, vocab

  def __call__(self, text):
    text = self.clean(text)
    if self.bow:
      text = self.clean_bow(text)
    return text

  # Given an iterable or dict where keys are vocab terms
  #  return a map where keys are terms and values are feature indices
  def vocab_to_indices(self, vocab):
    terms = vocab
    if isinstance(vocab, dict):
      terms = vocab.keys()
    vocab_indices = {}
    term_i = 0
    for term in terms:
      vocab_indices[term] = term_i
      term_i += 1
    return vocab_indices

  # Return clean text and set of vocab
  # sent_tokenize, word_tokenize, lowercase, stem, remove stops
  def clean_text_vocab(self, text):
    processed_text = ""

    for ch in text:
      if ch in self.expand:
        processed_text += " "+ch+" "
      else:
        processed_text += ch.lower()
    cleaned_text = ""
    # Put space between numbers and letters
    processed_text = re.sub(self.wordnum_pattern, self.wordnum_replace, processed_text)
    for sentence in sent_tokenize(processed_text):
      for word in word_tokenize(sentence):
        if word and word not in self.stop_words:
          word = self.stemmer.stem(word)
          cleaned_text += " "+word
          self.clean_vocab[word] += 1
    return cleaned_text.strip()

  # For a list of texts, return list of clean texts and set of vocab
  # source_file is a pickled binary file
  # dest_clean is the basename of where the clean text will go
  #   dest_clean.pkl has the pickled binary file
  #   dest_clean.txt has the plain text
  # vocab_file is the basename for the vocab binary and plain text
  def clean_texts_vocab(self, source_file, dest_clean_file=None, vocab_file=None, texts=None):
    start()
    vprint(source_file, 'Cleaning text at')
    if not dest_clean_file:
      dest_clean_file = add_file_suffix(source_file, 'clean')
    if not vocab_file:
      vocab_file = add_file_suffix(dest_clean_file, 'vocab')
    if texts is None:
      texts = vload(source_file)
    clean_texts = []
    for text in texts:
      clean_texts.append(self.clean_text_vocab(text))
    # Save texts
    # Make sure there's no extension
    dest_clean_file, ext = os.path.splitext(dest_clean_file)
    vsave(clean_texts, dest_clean_file+'.pkl') # binary
    vsave(clean_texts, dest_clean_file+'.txt') # txt
    # Save vocab
    vocab_file, ext = os.path.splitext(vocab_file)
    vsave(self.clean_vocab, vocab_file+'.pkl')
    vsave(self.clean_vocab, vocab_file+'.txt')
    self.clean_vocab_indices = self.vocab_to_indices(self.clean_vocab)
    vsave(self.clean_vocab_indices, vocab_file+'_indices.pkl')
    lprint(self.clean_vocab, 'Clean vocab')
    end("Finished cleaning")
    lprint(self.clean_vocab_indices)
    return dest_clean_file+'.pkl', clean_texts

  def clean_bow(self, text):
    punc_free = re.sub(self.remove_pattern, ' ', text)
    space_normed = re.sub(self.extra_space_pattern, ' ', punc_free).strip() # Only allow one contiguous space
    return space_normed

  # Given clean text, clean more (for bag of words type use):
  #  Remove punctuation
  #  Only keep a-z, 0-9, : (for scripture references)
  def clean_to_bow_text(self, text):
    # punc_free = text.translate(self.punc_trans)
    space_normed = self.clean_bow(text)
    for word in space_normed.split():
      self.bow_vocab[word.strip()] += 1 # Remove any new lines or other spacing here
    return space_normed

  # Given clean text, clean more (for bag of words type use):
  #  Remove punctuation
  #  Only keep a-z, 0-9, : (for scripture references)
  def clean_to_bow_vocab(self, source_file, dest_clean_file=None, vocab_file=None, texts=None):
    start()
    vprint(source_file, 'Bow cleaning text at')
    if not dest_clean_file:
      dest_clean_file = add_file_suffix(source_file, 'bow')
    if not vocab_file:
      vocab_file = add_file_suffix(dest_clean_file, 'vocab')
    if texts is None:
      texts = vload(source_file)
    clean_texts = []
    for text in texts:
      punc_free = self.clean_to_bow_text(text)
      clean_texts.append(punc_free)
    # Save texts
    # Make sure there's no extension
    dest_clean_file, ext = os.path.splitext(dest_clean_file)
    vsave(clean_texts, dest_clean_file+'.pkl') # binary
    vsave(clean_texts, dest_clean_file+'.txt') # txt
    # Save vocab
    vocab_file, ext = os.path.splitext(vocab_file)
    vsave(self.bow_vocab, vocab_file+'.pkl')
    vsave(self.bow_vocab, vocab_file+'.txt')
    self.bow_vocab_indices = self.vocab_to_indices(self.bow_vocab)
    vsave(self.bow_vocab_indices, vocab_file+'_indices.pkl')
    lprint(self.bow_vocab, 'BOW clean vocab')
    end("Finished BOW cleaning")
    return dest_clean_file+'.pkl', clean_texts

# exclude = set(string.punctuation)
# exclude |= set(['—','–','-'])
# punc_trans = str.maketrans(dict.fromkeys(exclude, ' '))
# text = 'test.) -other 49 : 7:8 2:7mark mark27'
# vprint(text)
# remove_pattern = re.compile(r'[^\p{L}\p{N}:\s]|\s:\s]')
# text = re.sub(r'(\p{L})(\p{N})|(\p{N})(\p{L})', r'\1\3 \2\4', text)
# vprint(text)
# punc_free = re.sub(remove_pattern, ' ', text)
# vprint(punc_free)
# punc_free = re.sub(' {2,}', ' ', punc_free)
# vprint(punc_free)
# processor = ReligiousTextProcessor()
# text = processor.clean_text_vocab(text)
# vprint(text)
