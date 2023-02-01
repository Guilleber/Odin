from typing import List, Dict, Union, Any
from tqdm import tqdm
from pprint import pprint

from .metadata_tools import getMetadata

import pymongo
import os
import sys


DATABASE_NAME = "PhotoStorage"
DEFAULT_COLLECTION_NAME = "Default"


ON_EXISTS_VALUES = [
    'rename',
    'replace'
]


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


class MongoInterface:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        self.database = client[DATABASE_NAME]
        self.collection = self.database[DEFAULT_COLLECTION_NAME]


    def config(self):
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

        progbar = tqdm(total=len(file_list), file=sys.stdout)
        for files in batch(file_list, 10):
            metadata = getMetadata(files)
            
            for m in metadata:
                try:
                    self.collection.insert_one(m)
                except Exception as e:
                    skipped += 1

            progbar.update(len(files))
            progbar.refresh()

        progbar.close()

        print("Finished: {} added, {} skipped".format(len(file_list) - skipped, skipped))
        
    
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
