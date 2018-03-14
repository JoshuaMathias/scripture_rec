import sys
import argparse
from recommenders import recommenders
from source_types import Bible, recommendations_source

# Program to recommend Bible verses. Receives from standard in. Outputs to standard out.

argParser = argparse.ArgumentParser(description="Program to recommend Bible verses. Receives input from standard in. Outputs recommendations to standard out.")
argParser.add_argument('command', choices=["train", "test", "run_all"], help="Train recommendation model, test using pre-trained model, or both (run_all).")
argParser.add_argument('-t', '--train_path', default="data/kjvdat.txt", help="The filepath of the training data. Defaults to data/kjvdat.txt")
argParser.add_argument('-l', '--model_path', default="data/model.lda", help="Filepath from which to load the trained recommendation model")
argParser.add_argument('-i', '--input_path', default=sys.stdin, help="The filepath of the input from which to base recommendations (separated by new line). Defaults to standard in.")
argParser.add_argument('-s', '--source_path', default="data/kjvdat.txt", help="The source from which to recommend items or passages. Defaults to data/kjvdata.txt (the Bible).")
argParser.add_argument('-p', '--source_type', choices=["book", "bible"], default="bible", help="The type of recommendation source. Defaults to 'bible'.")
argParser.add_argument('-m', '--method', choices=["tdlm","lda","td-idf"], default="lda", help="Recommendation system implementation.")
args = argParser.parse_args()

if args.source_type == "bible":
    source = Bible(args.source_path)
else:
    source = recommendations_source.RecommendationSource(args.source_path)

recommender = recommenders.getRecommender(args.method)
recommender.source(source)

if args.command == "train" or args.command == "run_all":
    if not args.train_path:
        raise ValueError("--train_path must be specified to perform training")
    recommender.train(args.train_path)

if args.input_path is sys.stdin:
    inputSource = sys.stdin
else:
    inputSource = open(args.input_path, 'r')

for line in inputSource:
    line = line.strip()
    if line:
        print("input: "+line)
        print(recommender.recommend(line))
