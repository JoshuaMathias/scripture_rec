import bible_object
import bible_ref_data_creator
import os

foundEn = False
foundTxt = False
enBooks = {}
# indexPattern = re.compile("\/(\d+)[\w\-_]*.txt")

bible = bible_object.Bible(numWordMatch=0)
refDataFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","bible_book_names.txt")
refFinder = bible_ref_data_creator.ReferenceFinder(bible, refDataFile)

for line in open('/home2/emathias/thesis/gutenberg_english.txt'):
    line = line.strip()
    if len(line):
        splitLine = line.split()
        if len(splitLine) > 1:
            indexStr = splitLine[0]
            path = splitLine[1]
            enBooks[indexStr] = path

chosenBooks = []
booksLists = ['data/gutenberg_mormon_books.txt','data/gutenberg_religion_books.txt','data/gutenberg_bible_books.txt']
outFile = open('/home2/emathias/thesis/gutenberg_bible_refs.txt', 'a+')
for booksList in booksLists:
    booksCount = 0
    unFoundCount = 0
    for index in open(booksList, 'r'):
        index = index.strip()
        if index in enBooks:
            booksCount += 1
            chosenBooks.append(index)
            with open(enBooks[index], 'r') as bookFile:
                print("Getting references for file "+enBooks[index])
                refStr = refFinder.printBibleReferences(bookFile.read())
                outFile.write(refStr)
        else:
            unFoundCount += 1
#     print("English text books found from "+booksList+" - "+str(booksCount))
#     print("English text books not found from "+booksList+" - "+str(unFoundCount))
# print("Total English text books found: "+str(len(chosenBooks)))


