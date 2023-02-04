import os
import argparse
import jsondatetime as json

from .config import *
from .mdb import MongoInterface


def main():
    parser = argparse.ArgumentParser(description="Command line interface for Odin")
    subparsers = parser.add_subparsers(dest="verb")
    subparsers.required = True

    #start
    start_parser = subparsers.add_parser('start')

    #stop
    stop_parser = subparsers.add_parser('stop')

    #init
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('-c', '--collection', type=str, default=DEFAULT_COLLECTION_NAME,
                        help="the name of the mongodb collection")

    #add
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('paths', metavar='PATH', type=str, nargs='+',
                            help="a path to be added to the tracking system")
    add_parser.add_argument('-c', '--collection', type=str, default=DEFAULT_COLLECTION_NAME,
                        help="the name of the mongodb collection")

    #rm
    rm_parser = subparsers.add_parser('rm')
    rm_parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="a mongodb query describing what to find")
    rm_parser.add_argument('-c', '--collection', type=str, default=DEFAULT_COLLECTION_NAME,
                        help="the name of the mongodb collection")

    #find
    find_parser = subparsers.add_parser('find')
    find_parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="a mongodb query describing what to find")
    find_parser.add_argument('-c', '--collection', type=str, default=DEFAULT_COLLECTION_NAME,
                        help="the name of the mongodb collection")

    #mv
    mv_parser = subparsers.add_parser('mv')
    mv_parser.add_argument('query', metavar='QUERY', type=json.loads,
                        help="a mongodb query describing what to move")
    mv_parser.add_argument('dest', metavar='DEST', type=str,
                        help="the destination directory")
    mv_parser.add_argument('-c', '--collection', type=str, default=DEFAULT_COLLECTION_NAME,
                        help="the name of the mongodb collection")
    mv_parser.add_argument('--on_exists', metavar='OE', type=str,
                        choices=ON_EXISTS_VALUES, default='rename',
                        help="what to do when a file with the same name already exists")

    args = parser.parse_args()

    if args.verb == 'start':
        os.system('sudo systemctl start mongod')
        return
    elif args.verb == 'stop':
        os.system('sudo systemctl stop mongod')
        return

    db = MongoInterface(collection=args.collection)

    if args.verb == 'init':
        db.init_database()
    elif args.verb == 'add':
        db.add(args.paths)
    elif args.verb == 'rm':
        db.remove(args.query)
    elif args.verb == 'find':
        db.find(args.query)
    elif args.verb == 'mv':
        db.move(args.query, args.dest, on_exists=args.on_exists)

    return


if __name__ == "__main__":
    main()
