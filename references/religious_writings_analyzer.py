# import bible_object
# import bible_ref_data_creator
# import os
from cleanup import strip_headers

foundEn = False
foundTxt = False
enBooks = {}
# indexPattern = re.compile("\/(\d+)[\w\-_]*.txt")

# bible = bible_object.Bible(numWordMatch=0)
# refDataFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","bible_book_names.txt")
# refFinder = bible_ref_data_creator.ReferenceFinder(bible, refDataFile)

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
            with open(enBooks[index], 'r') as book_file:
                book_text = strip_headers(book_file.read())
                print("Book ID: "+str(index)+" "+enBooks[index])
                book_third_1 = int(len(book_text)/3)
                book_third_2 = book_third_1*2
                book_selection = book_text[:1000]+"\n"+book_text[book_third_1:book_third_1+1000]+"\n"+book_text[book_third_2:book_third_2+1000]+"\n"+book_text[-1000:]
                print(book_selection+"\n")
                # print("Getting references for file "+enBooks[index])
                # refStr = refFinder.printBibleReferences(book_file.read())
                # outFile.write(refStr)
        else:
            unFoundCount += 1
#     print("English text books found from "+booksList+" - "+str(booksCount))
#     print("English text books not found from "+booksList+" - "+str(unFoundCount))
# print("Total English text books found: "+str(len(chosenBooks)))
