import argparse
import os
from cleanup import strip_headers
import preprocessing


class ReferenceFinder:
    def __init__(self):
        self.passages = []
        self.references = {}

    def writeDocumentRefs(self, doc_path, doc_out_path):
        ref_writer = open(doc_out_path, 'w')
        with open(doc_path, 'r') as file:
            file_lines = strip_headers(file.read()).split("\n")
            lineI = 0
            line = ""
            while lineI < len(file_lines): # Skip table of contents
                line = file_lines[lineI].strip()
                if line.startswith("Index") or line.startswith("INDEX"): # Table of contents ends with index
                    break
                lineI += 1

            sectionName = ""
            while lineI < len(file_lines): # Go to the start of the first section
                line = file_lines[lineI].strip().lower()
                if line.startswith("chapter"):
                    sectionName = "chapter"
                    break
                elif line.startswith("lecture"):
                    sectionName = "lecture"
                    break
                lineI += 1
            while lineI < len(file_lines):
                line = file_lines[lineI].strip().lower()
                self.addPassage(line, lineI)


    # Creates and stores a Passage object, with any references found in the text.
    def addPassage(self, text, lineI):
        references = []
        tokens, textStr = preprocessing.tokenizeTuple(text)
        newPassage = Passage(textStr, lineI)


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
    argParser = argparse.ArgumentParser(description="Create a dataset of passages and references that accompany them.")
    argParser.add_argument("writings_dir",help="The directory containing documents from which to create a dataset.")
    args = argParser.parse_args()

    refFinder = ReferenceFinder()


    for filename in os.listdir(args.writings_dir):
        passages = [] # Selected passages
        footnotes = [] # Indexed footnotes of references, corresponding to a passage.
        filepath = os.path.join(args.writings_dir, filename)
        refFinder.addDocument(filepath)

if __name__== "__main__":
    main()