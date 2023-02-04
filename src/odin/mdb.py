from typing import List, Dict, Union, Any
from tqdm import tqdm
from pprint import pprint

from .utils.metadata_tools import getMetadata
from .config import *

import pymongo
import os
import sys


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


class MongoInterface:
    def __init__(self, collection=DEFAULT_COLLECTION_NAME):
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        self.database = client[DATABASE_NAME]
        self.collection = self.database[collection]


    def init_database(self):
        self.collection.create_index([("directory", pymongo.ASCENDING),
            ("filename", pymongo.ASCENDING)], unique=True)


    def add(self, paths: Union[str, List[str]]) -> None:
        if type(paths) is str:
            paths = [paths]

        file_list = []

        for path in paths:
            if not os.path.exists(path):
                raise FileNotFoundError("No such file or directory: {}".format(path))

            if os.path.isfile(path):
                file_list.append(path)
            else:
                for root, _, files in os.walk(path):
                    for filename in files:
                        file_list.append(os.path.join(root, filename))

        print("Adding {} files...".format(len(file_list)))

        skipped = 0

        for file in tqdm(file_list, file=sys.stdout):
            metadata = getMetadata(file)
            
            try:
                self.collection.insert_one(metadata)
            except Exception as e:
                skipped += 1

        print("Finished: {} added, {} skipped".format(len(file_list) - skipped, skipped))


    def remove(self, query: Dict[str, Any]) -> None:	
        res = self.collection.delete_many(query)
        print("{} files removed".format(res.deleted_count))
        
    
    def _find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return list(self.collection.find(query))


    def find(self, query: Dict[str, Any]) -> None:
        results = self._find(query)

        print("Found {} files...".format(len(results)))

        pprint(results)


    def _move(self, entry: Dict[str, Any], dest: str, on_exists='rename') -> None:
        if entry['directory'] == dest:
            return

        filename = entry['filename']

        if on_exists == 'replace':
            self.collection.delete_one({'directory': dest, 'filename': filename})
        elif on_exists == 'rename':
            if os.path.exists(os.path.join(dest, filename)):
                num = 1
                name, ext = filename.split('.', 1)
                filename_temp = name + "-{}." + ext
                filename = filename_temp.format(num)

                while os.path.exists(os.path.join(dest, filename)):
                    num += 1
                    filename = filename_temp.format(num)
        else:
            raise ValueError("Invalid value '{}' for argument on_exist".format(on_exists))

        os.rename(os.path.join(entry['directory'], entry['filename']), os.path.join(dest, filename))
        self.collection.update_one({'_id': entry['_id']}, {'$set': {'directory': dest, 'filename': filename}})


    def move(self, query: Dict[str, Any], dest: str, **kwargs) -> None:
        results = self._find(query)
        dest = os.path.abspath(dest)

        print("Moving {} files to {}".format(len(results), dest))

        for entry in tqdm(results):
            self._move(entry, dest, **kwargs)
