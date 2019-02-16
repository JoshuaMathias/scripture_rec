# %%writefile scripture-rec/source_types/scripture_object.py

# Return formatted str of verse in dat format
# chapter_i and verse_i start at 0 (1 below actual chapter and verse number)
def verse_dat(book_name, chapter_i, verse_i, text):
  return book_name + "|" + str(chapter_i+1) + "|" + str(verse_i+1) \
      + "| " + text + "~"


class Verse:
  def __init__(self, text, book, chapter, verse_i, index=-1):
      self.text = text
      self.book = book
      self.chapter = chapter
      self.verse_i = verse_i
      self.name = str(self.verse_i+1)
      self.index = index
      self.score = 0
      self.refs = [] # Reference objects
      self.encoding = None
      self.embedding = None
      self.vector = None
      self.contexts = [] # Tuples of (context_id, weight)
      self.used_features = None
      self.sum_squares = None

  def calc_used_features(self, vector=None):
    self.used_features = []
    if not vector:
      vector = self.vector
    for i in range(len(vector)):
      if vector[i]:
        self.used_features.append(i)

  def calc_sum_squares(self, vector=None):
    if not vector:
      vector = self.vector
    for i in self.used_features:
      self.sum_squares += vector[i]**2
    self.sum_squares = math.sqrt(self.sum_squares)

  # Return nicely formatted verse
  def print(self):
    return verse_dat(self.book.name, self.chapter.chapter_i, self.verse_i, self.text)

  def __str__(self):
    return "Verse "+self.book.name+" "+self.chapter.name+":"+self.name+" index: "+str(self.index)+" score: "+str(self.score)+" text: "+str(self.text)

  def __lt__(self, other):
    return self.score < other.score


class Chapter:
    def __init__(self, book, chapter_i, index=-1):
        self.book = book
        self.chapter_i = chapter_i
        self.name = str(self.chapter_i+1)
        self.verses = []
        self.score = 0
        if index != -1:
          self.index = index
        elif len(verses) > 0:
          self.index = verses[0].index
        else:
          self.index = -1

    def __str__(self):
        return "Chapter "+str(self.book.name)+" "+str(self.chapter_i+1)+" index: "+str(self.index)+" verses: "+str(len(self.verses))+" score: "+str(self.score)

    def __lt__(self, other):
        return self.score < other.score
      
    def add_verse(self, verse):
      if len(self.verses) == 0:
        self.index = verse.index
      self.verses.append(verse)

    def get_verses(self):
      return self.verses

class Book:
    def __init__(self, name, volume, book_i, index=-1):
        self.name = name
        self.book_i = book_i
        self.volume = volume
        self.chapters = []
        self.index = index

    def __str__(self):
        return "Book of "+self.name+": book_i: "+str(self.book_i)+" index: "+str(self.index)+\
        " chapters: "+str(len(self.chapters))

    def __lt__(self, other):
        return self.book_i < other.book_i
      
    def add_chapter(self, chapter):
      if len(self.chapters) == 0:
        self.index = chapter.index
      self.chapters.append(chapter)

    def get_verses(self):
      verses = []
      for chapter in self.chapters:
        verses.extend(chapter.get_verses())
      return verses

class Volume:
    def __init__(self, name, collection_i, index=-1):
        self.name = name
        self.volume_i = collection_i
        self.books = []
        self.index = index

    def __str__(self):
        return "Volume "+self.name+"  index: "+str(self.index)+\
        " books: "+str(len(self.books))

    def __lt__(self, other):
        return self.collection_i < other.collection_i
      
    def add_book(self, book):
      if len(self.books) == 0:
        self.index = book.index
      self.books.append(book)

    def get_verses(self):
      verses = []
      for book in self.books:
        verses.extend(book.get_verses())
      return verses
      
class Collection:
    def __init__(self, name, collection_i, index=-1):
        self.name = name
        self.collection_i = collection_i
        self.volumes = []
        self.books = []
        self.index = index

    def __str__(self):
        return "Collection "+self.name+"  index: "+str(self.index)+\
        " Volumes: "+str(len(self.volumes))

    def __lt__(self, other):
        return self.collection_i < other.collection_i
      
    def add_volume(self, volume):
      if len(self.volumes) == 0:
        self.index = volume.index
      self.volume.append(volume)      

    def get_verses(self):
      verses = []
      for volume in self.volumes:
        verses.extend(volume.get_verses())
      return verses

      
def contains_alpha(text):
    for char in text:
        if char.isalpha():
            return True
    return False


class Scripture:
    def __init__(self, filename="", num_word_match=0):
#         super()
        self.filename = filename
        if not len(self.filename):
            self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","kjvdat.txt")
        self.collections = []
        self.collection_names = {}
        self.volumes = []
        self.volume_names = {}
        self.books = []
        self.book_names = {}
        self.chapters = []
        self.verses = []
        self.trie = None
        if self.filename.endswith('.csv'):
          dat_filename = self.filename.replace('.csv', '.txt')
          self.csv_to_dat(self.filename, dat_filename)
          self.filename = dat_filename
          self.parse_dat(num_word_match)
        else:
          self.parse_dat(num_word_match)
        self.verse_encodings = None
        self.verse_embeddings = None
    
    # Return true if the scripture reference exists in the Bible.
    # Book is an id.
#     def is_valid_ref(self, book, chapter, verse):

    # Return a list of verses from the book (str), chapter, and verse(s) in the chapter.
    def reference_to_verses(self, book_name, chapter_i, verses_i):
      if book_name in self.book_names:
        try:
          book = self.book_names[book_name]
          verses = []
          chapter = book.chapters[chapter_i-1]
          if len(verses_i):
            for verse_i in verses_i:
              verses.append(chapter.verses[verse_i-1])
          else:
            for verse in chapter.verses:
              verses.append(verse)
          return verses
        except IndexError:
          return False
      else:
        return False
      
    # Return a list of verse IDs from the book (str), chapter, and verse(s) in the chapter.
    def reference_to_verse_ids(self, book_name, chapter_i, verses):
      if book_name in self.book_names:
        try:
          book = self.book_names[book_name]
          verse_ids = []
          chapter = book.chapters[chapter_i-1]
          if len(verses):
            for verse_i in verses:
              verse_ids.append(chapter.verses[verse_i-1].index)
          else:
            for verse in chapter.verses:
              verse_ids.append(verse.index)
          return verse_ids
        except IndexError:
          return False
      else:
        return False
    
    # Return a list of verse IDs from the book (str), chapter, and verse.
    def reference_to_verse_id(self, book_name, chapter_i, verse_i):
      if book_name in self.book_names:
        try:
          return self.book_names[book_name].chapters[chapter_i-1].verses[verse_i-1].index
        except IndexError:
          return False
      else:
        return False
      
    # Return book (str), chapter, and verse from a given verse ID.
    def verse_id_to_reference(self, verse_id):
      verse = self.verses[verse_id]
      return verse.book.name, verse.chapter.name, verse.name
       
    # Add every sequence of num_word_match tokens to the trie.
    def add_to_trie(self, tokens, verse, num_word_match=4):
        currentTokens = []
        for word in tokens:
            if contains_alpha(word): # Skip punctuation tokens
                currentTokens.append(word)
                if len(currentTokens) > num_word_match:
                    currentTokens.pop(0)
                    phrase = " ".join(str(e) for e in currentTokens)
                    if not self.trie.has_node(phrase):
                        self.trie[phrase] = [verse]
                    else:
                        self.trie[phrase].append(verse)

     # Parse format of data/kjvdat.txt
    # num_word_match is the minimum sequence of words for which verse references are saved in the trie. If 0, no trie is initialized.
    def parse_dat(self, num_word_match=4):
        curr_volume_i = 0 # order of current volume
        volume = Volume("", 0) # current Volume
        self.volumes.append(volume)
        curr_book = "" # name of current book
        book = None # current Book
        curr_book_i = 0 # order of current book
        chapter = None # current Chapter
        curr_chapter = 0 # last chapter_i parsed
        curr_index = 0 # order of current verse
        curr_verses = []
        curr_chapters = []
        if num_word_match > 0:
            self.trie = pygtrie.StringTrie(separator=" ")
        with open(self.filename, 'r') as scripture_file:
          for line in scripture_file:
              split_line = line.split("|")
              if len(split_line) == 1:
                vol_name = line.strip()
                if book: # If we're past the first volume of books
                  volume = Volume(vol_name, curr_volume_i)
                  self.volumes.append(volume)
                volume.name = vol_name
                print("volume name: "+str(volume.name))
                self.volume_names[volume.name] = volume
                volume.volume_i = curr_volume_i
                curr_volume_i += 1
              elif len(split_line) > 2:
                book_name = split_line[0]
                chapter_i = int(split_line[1])-1
                verse_i = int(split_line[2])-1
                text = split_line[3].strip()[:-1] # Remove initial space and trailing ~
                if book_name != curr_book:

                    curr_book = book_name
                    book = Book(book_name, volume, curr_book_i)
                    self.books.append(book)
                    self.book_names[book_name] = book
                    
                    curr_book_i += 1

                    chapter = Chapter(book, chapter_i, index=curr_index)
  #                   print("adding chapter "+str(chapter_i)+" to book "+str(book.name))
                    book.add_chapter(chapter)
                    self.chapters.append(chapter)
                    curr_chapter = chapter_i
                    volume.add_book(book)
                elif chapter_i != curr_chapter: # If in the same book, but the chapter has changed
                    curr_chapter = chapter_i
                    chapter = Chapter(book, chapter_i, index=curr_index)
  #                   print("adding chapter "+str(chapter_i)+" to book "+str(book.name))
                    book.add_chapter(chapter)
                    self.chapters.append(chapter)

                new_verse = Verse(text, book, chapter, verse_i, curr_index)
                chapter.add_verse(new_verse)
                self.verses.append(new_verse)
                curr_index += 1
                if num_word_match > 0:
                    self.add_to_trie(tokens, newVerse)
        print("Parsed "+self.filename+" with "+str(len(self.volumes))+" volumes, "+str(len(self.books))+" books, "+str(len(self.chapters))+" chapters, "+str(len(self.verses))+" verses")
       
    # Convert csv of scriptures to dat (simplified) format
    def csv_to_dat(self, csv_filename, dat_filename):
      import csv
      headers = ['volume_id','book_id','chapter_id','verse_id','volume_title','book_title','volume_long_title','book_long_title','volume_subtitle','book_subtitle','volume_short_title','book_short_title','volume_lds_url','book_lds_url','chapter_number','verse_number','scripture_text','verse_title','verse_short_title']
      headers_dict = {}
      header_i = 0
      for header in headers:
        headers_dict[header] = header_i
        header_i += 1
      with open(csv_filename, 'r') as csv_file:
        with open(dat_filename, 'w') as dat_file:
          csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
          next(csv_reader)
          curr_volume_name = ''
          for row in csv_reader:
            new_vol = row[headers_dict['volume_lds_url']]
            new_book = row[headers_dict['book_lds_url']]
            chapter_num = int(row[headers_dict['chapter_number']])
            verse_num = int(row[headers_dict['verse_number']])
            verse_text = row[headers_dict['scripture_text']]
            
            if new_vol != curr_volume_name:
              curr_volume_name = new_vol
              dat_file.write(curr_volume_name+"\n")
            verse_str = verse_dat(new_book, int(chapter_num)-1, int(verse_num)-1, verse_text)
            dat_file.write(verse_str+"\n")
            
    # Write Scripture object to file in dat txt format
    def write_all(self, filename):
      with open(filename, 'w') as file:
        for volume in self.volumes:
          file.write(volume.name+"\n")
          for verse in volume.get_verses():
            file.write(verse.print()+"\n")
      
