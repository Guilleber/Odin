from typing import List, Union
from tqdm import tqdm

from .metadata_tools import getMetadata

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
                    for filename in files:
                        file_list.append(os.path.join(root, filename))

        print("Adding {} files...".format(len(file_list)))

        skipped = 0

        for file in tqdm(file_list):
            metadata = getMetadata(file)[0]

            try:
                self.collection.insert_one(metadata)
            except:
                skipped += 1

        print("Finished: {} added, {} skipped".format(len(file_list) - skipped, skipped))
        
        
