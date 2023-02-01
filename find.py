import jsondatetime as json
import argparse

from utils.mongo_tools import MongoInterface


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find files")
    parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="a mongodb query describing what to find")

    args = parser.parse_args()

    mongo = MongoInterface()
    mongo.find(args.query)
