import exiftool
import os

from typing import Dict, List, Union, Any


META_NAME_MAP = {
    'File:FileName': 'FileName',
    'File:Directory': 'Directory',
}

META_TYPE = {
    'File:FileName': str,
    'File:Directory': os.path.abspath,
}


et = exiftool.ExifToolHelper()


def getExif(imname: Union[str, List[str]]) -> List[Dict[str, Any]]:
    return et.get_metadata(imname)


def exif2Meta(exif: Dict[str, Any]) -> Dict[str, Any]:
    meta = {META_NAME_MAP[k]: META_TYPE[k](exif[k]) for k in META_NAME_MAP if k in exif}
    return meta


def getMetadata(imname: Union[str, List[str]]) -> List[Dict[str, Any]]:
    exifs = getExif(imname)
    metas = [exif2Meta(ex) for ex in exifs]

    return metas
        
