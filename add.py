from utils.mongo_tools import MongoInterface

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add files to tracking")
    parser.add_argument('paths', metavar='PATH', type=str, nargs='+',
                        help="a path to be added to the tracking system")

    args = parser.parse_args()

    mongo = MongoInterface()
    mongo.add(args.paths)
