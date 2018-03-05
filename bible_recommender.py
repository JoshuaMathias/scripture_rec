import sys
import argparse
import bible_object
import recommenders

# Program to recommend Bible verses. Receives from standard in. Outputs to standard out.

argParser = argparse.ArgumentParser(description="Program to recommend Bible verses. Receives input from standard in. Outputs recommendations to standard out.")
argParser.add_argument('-b', '--bible_path', default="data/kjvdat.txt", help="The filepath of the Bible corpus. Defaults to data/kjvdat.txt")
argParser.add_argument('-m', '--method', choices=["tdlm","lda","td-idf"], default="lda", help="Recommendation system implementation")
args = argParser.parse_args()

if args.bible_path:
    bible_path = args.bible_path

source = bible_object.Bible(bible_path)

recommender = recommenders.recommender(args.method)
recommender.source(source)
# if args.method == "tdlm":
#     print("Using TDLM")
#     recommender = recommenders.recommender("tdlm")
# elif args.method == "lda":
#     print("Using LDA")
# elif args.method == "td-idf":
#     print("Using TD-IDF")

for line in sys.stdin:
    print("input: "+line)
    print(recommender.recommend(line))
