import exiftool
import os

from typing import Dict, List, Union, Any
from datetime import datetime


META_NAME_MAP = {
    'EXIF:ISO': 'iso',
    'EXIF:ApertureValue': 'aperture',
    'EXIF:ExposureTime': 'exposure_time',
    'EXIF:FocalLength': 'focal_length',
    'EXIF:Flash': 'flash',
}

META_TYPE = {
    'EXIF:ISO': int,
    'EXIF:ApertureValue': float,
    'EXIF:ExposureTime': float,
    'EXIF:FocalLength': int,
    'EXIF:Flash': bool,
}


et = exiftool.ExifToolHelper()


def getExif(filepath: Union[str, List[str]]) -> List[Dict[str, Any]]:
    return et.get_metadata(filepath)


def _extractExif(exif: Dict[str, Any]) -> Dict[str, Any]:
    metas = {META_NAME_MAP[k]: META_TYPE[k](exif[k]) for k in META_NAME_MAP if k in exif}

    if 'EXIF:Make' in exif and 'EXIF:Model' in exif:
        metas['camera'] = exif['EXIF:Make'] + ' ' + exif['EXIF:Model']

    if 'EXIF:LensMake' in exif and 'EXIF:LensModel' in exif:
        metas['lens'] = exif['EXIF:LensMake'] + ' ' + exif['EXIF:LensModel']
    
    return metas


def getExifMeta(filepaths: List[str]) -> List[Dict[str, Any]]:

    try:
        exif = getExif(filepaths)
    except:
        return [{} for _ in filepaths]
    
    return [_extractExif(e) for e in exif]


def _getFileMeta(filepath: str) -> Dict[str, Any]:
    metas = dict()

    directory, filename = os.path.split(filepath)
    metas['filename'] = filename
    metas['directory'] = os.path.abspath(directory)

    metas['date'] = datetime.fromtimestamp(os.path.getmtime(filepath))

    return metas


def getFileMeta(filepaths: List[str]) -> List[Dict[str, Any]]:
    return [_getFileMeta(f) for f in filepaths]


META_FUNC = [
    getFileMeta,
    getExifMeta,
]


def getMetadata(filepaths: List[str]) -> List[Dict[str, Any]]:
    metas = [dict() for _ in filepaths]

    for getMeta in META_FUNC:
        new_metas = getMeta(filepaths)

        for i in range(len(filepaths)):
            metas[i].update(new_metas[i])

    for i in range(len(filepaths)):
        metas[i]['date_added'] = datetime.now()

    return metas
        
