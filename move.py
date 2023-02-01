import jsondatetime as json
import argparse

from utils.mongo_tools import MongoInterface, ON_EXISTS_VALUES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move files")
    parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="a mongodb query describing what to move")
    parser.add_argument('dest', metavar='DEST', type=str,
                        help="the destination directory")
    parser.add_argument('--on_exists', metavar='OE', type=str,
                        choices=ON_EXISTS_VALUES, default='rename',
                        help="what to do when a file with the same name already exists")

    args = parser.parse_args()

    mongo = MongoInterface()
    mongo.move(args.query, args.dest, on_exists=args.on_exists)
