import pygtrie
from cleanup.preprocessing import tokenizeTuple
import os
from source_types.recommendations_source import RecommendationsSource


class Verse:
    def __init__(self, text, bookI, chapter, verse, index=-1):
        self.text = text
        self.bookI = bookI
        self.chapter = chapter
        self.verse = verse
        self.index = index
        self.score = 0

    def __str__(self):
        return "Verse "+str(self.bookI)+" "+str(self.chapter)+":"+str(self.verse)+" score: "+str(self.score)

    def __lt__(self, other):
        return self.score < other.score


class Chapter:
    def __init__(self, bookI, chapter, verses):
        self.bookI = bookI
        self.chapter = chapter
        self.verses = verses
        self.score = 0

    def __str__(self):
        return "Chapter "+str(self.bookI)+" "+str(self.chapter)+" score: "+str(self.score)

    def __lt__(self, other):
        return self.score < other.score


def containsAlpha(text):
    for char in text:
        if char.isalpha():
            return True
    return False


class Bible(RecommendationsSource):
    def __init__(self, filename=""):
        super()
        self.filename = filename
        if not len(self.filename):
            self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","kjvdat.txt")
        self.books = []
        self.chapters = []
        self.verses = []
        self.trie = None
        # self.parseBible(numWordMatch)

    def referenceToVerse(self, bookI, chapter, verse):
        return (bookI+1) * (chapter+1) * (verse+1)

    # Add every sequence of numWordMatch tokens to the trie.
    def addToTrie(self, tokens, verse, numWordMatch=4):
        currentTokens = []
        for word in tokens:
            if containsAlpha(word): # Skip punctuation tokens
                currentTokens.append(word)
                if len(currentTokens) > numWordMatch:
                    currentTokens.pop(0)
                    phrase = " ".join(str(e) for e in currentTokens)
                    if not self.trie.has_node(phrase):
                        self.trie[phrase] = [verse]
                    else:
                        self.trie[phrase].append(verse)

    # numWordMatch is the minimum sequence of words for which verse references are saved in the trie. If 0, no trie is initialized.
    def parseBible(self, numWordMatch=4):
        currBook = ""
        currBookI = -1
        currChapter = -1
        # currIndex = 0
        currVerses = []
        if numWordMatch > 0:
            self.trie = pygtrie.StringTrie(separator=" ")
        for line in open(self.filename, 'r'):
            splitLine = line.split("|")
            book = splitLine[0]
            chapter = int(splitLine[1])-1
            verse = int(splitLine[2])-1
            tokens, text = tokenizeTuple(splitLine[3][:-1].strip()) # Remove initial space and trailing ~
            if book != currBook:
                if currBookI > -1:
                    print("Num chapters in "+self.books[-1]+": "+str(currChapter+1))
                currBook = book
                self.books.append(book)
                currBookI += 1
                currChapter = 0
                if currBookI > 0: # Not the first book, since no chapter would have been parsed yet.
                    self.chapters.append(Chapter(currBookI, currChapter, currVerses))
                currVerses = []
            elif chapter != currChapter:
                currChapter += 1
                self.chapters.append(Chapter(currBookI, currChapter, currVerses))
                currVerses = []
            newVerse = Verse(text, currBookI, currChapter, verse)
            currVerses.append(newVerse)
            self.verses.append(Verse(text, currBookI, currChapter, verse))
            if numWordMatch > 0:
                self.addToTrie(tokens, newVerse)
        self.chapters.append(Chapter(currBookI, currChapter, currVerses)) # Append last chapter
        print("Parsed Bible with "+str(len(self.books))+" books, "+str(len(self.chapters))+" chapters, "+str(len(self.verses))+" verses")
