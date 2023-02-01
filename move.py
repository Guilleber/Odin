import jsondatetime as json
import argparse

from utils.mongo_tools import MongoInterface


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move files")
    parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="A mongodb query describing what to find")
    parser.add_argument('dest', metavar='DEST', type=str,
                        help="The destination directory")

    args = parser.parse_args()

    mongo = MongoInterface()
    mongo.move(args.query, args.dest)
