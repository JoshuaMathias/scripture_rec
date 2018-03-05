import argparse
import os
from cleanup import strip_headers
import bible_object
import preprocessing


class ReferenceFinder:
    def __init__(self, bible, refDataFile=""):
        self.bible = bible
        self.passages = []
        self.references = {}
        self.bibleBookNames = {}
        self.parseBibleData(refDataFile)

    # Creates and stores a Passage object, with any references found in the text.
    def addPassage(self, text, lineI):
        references = []
        tokens, textStr = preprocessing.tokenizeTuple(text)
        newPassage = Passage(textStr, lineI)

    def parseBibleData(self, refDataFile):
        with open(refDataFile, 'r') as dataFile:
            for line in dataFile:
                splitLine = line.split("\t")
                if len(splitLine) > 1:
                    self.bibleBookNames[splitLine[1]] = splitLine[0]

    def printBibleReferences(self, text):
        tokens = preprocessing.tokenize(text)
        numTokens = len(tokens)
        refStr = ""
        # for name in self.bibleBookNames:
        #     print("name: "+name)
        for tokenI in range(numTokens):
            token = tokens[tokenI]
            # print("token: "+token)
            if token in self.bibleBookNames and tokenI < numTokens-1:
                nextToken = tokens[tokenI+1]
                if nextToken[0].isdigit() or nextToken[0] == 'i' or nextToken[0] == 'x' or nextToken[0] == 'v':

                    if tokenI > 0:
                        refStr += tokens[tokenI-1]+" "
                    refStr += token+" "
                    refStr += nextToken+" "
                    if tokenI < numTokens-2:
                        refStr += tokens[tokenI+2]+" "
                    refStr += "\n"
                else:
                    print("unlikely ref: "+token)
        print(refStr)
        return refStr


class Passage:
    def __init__(self, text, lineI, references={}, verses=[]):
        self.text = text
        self.lineI = lineI
        self.references = references
        self.verses = verses

    def addReference(self, ref):
        self.references[ref.refID] = ref.lineI-self.lineI # Store the distance between the lines

    def resolveReference(self, ref, verse):
        self.verses


class Reference:
    def __init__(self, refID, lineI):
        self.refID = refID
        self.lineI = lineI


def main():
    argParser = argparse.ArgumentParser(description="Create a dataset of texts and bible references that accompany them.")
    argParser.add_argument("writings_dir",help="The directory containing documents from which to create a dataset.")
    args = argParser.parse_args()

    bible = bible_object.Bible(numWordMatch=0)
    refDataFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","bible_book_names.txt")
    refFinder = ReferenceFinder(bible, refDataFile)


    # for filename in os.listdir(args.writings_dir):
    #     passages = [] # Selected passages
    #     footnotes = [] # Indexed footnotes of Bible references, corresponding to a passage.
    #     filepath = os.path.join(args.writings_dir, filename)
    #     print("file to index: "+filepath)
    #     with open(filepath, 'r') as file:
    #         fileLines = strip_headers(file.read()).split("\n")
    #         lineI = 0
    #         line = ""
    #         while lineI < len(fileLines): # Skip table of contents
    #             line = fileLines[lineI].strip()
    #             if line.startswith("Index") or line.startswith("INDEX"): # Table of contents ends with index
    #                 break
    #             lineI += 1

    #         sectionName = ""
    #         while lineI < len(fileLines): # Go to the start of the first section
    #             line = fileLines[lineI].strip().lower()
    #             if line.startswith("chapter"):
    #                 sectionName = "chapter"
    #                 break
    #             elif line.startswith("lecture"):
    #                 sectionName = "lecture"
    #                 break
    #             lineI += 1
    #         while lineI < len(fileLines):
    #             line = fileLines[lineI].strip().lower()
    #             refFinder.addPassage(line, lineI)

if __name__== "__main__":
    main()