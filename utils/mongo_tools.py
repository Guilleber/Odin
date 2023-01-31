from typing import List, Union
from .exif_tools import getMetadata

import pymongo
import os


DATABASE_NAME = "PhotoStorage"
DEFAULT_COLLECTION_NAME = "Default"


class MongoInterface:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        self.database = client[DATABASE_NAME]
        self.collection = self.database[DEFAULT_COLLECTION_NAME]


    def config(self):
        self.collection.create_index([("Directory", pymongo.ASCENDING),
            ("FileName", pymongo.ASCENDING)], unique=True)


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
                    for name in files:
                        file_list.append(os.path.join(root, name))

        metadata = getMetadata(file_list)

        self.collection.insert_many(metadata, ordered=False)
        
        
