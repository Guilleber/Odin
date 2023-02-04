import os

from typing import Dict, List, Union, Any
from datetime import datetime
from exif import Image

from ..config import *


META_NAME_MAP = {
    'photographic_sensitivity': 'iso',
    'aperture_value': 'aperture',
    'exposure_time': 'exposure_time',
    'focal_length': 'focal_length',
    'flash': 'flash',
}

META_TYPE = {
    'photographic_sensitivity': int,
    'aperture_value': float,
    'exposure_time': float,
    'focal_length': float,
    'flash': bool,
}


def getExifMeta(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'rb') as f:
        img = Image(f)

    if not img.has_exif:
        return dict()
    
    metas = dict()

    for key in META_NAME_MAP:
        try:
            metas[META_NAME_MAP[key]] = META_TYPE[key](img[key])
        except AttributeError:
            pass
    
    try:
        metas['camera'] = img['make'] + ' ' + img['model']
    except AttributeError:
        pass

    try:
        metas['lens'] = img['lens_make'] + ' ' + img['lens_model']
    except AttributeError:
        pass
    
    return metas


def getFileMeta(filepath: str) -> Dict[str, Any]:
    metas = dict()

    directory, filename = os.path.split(filepath)
    metas['filename'] = filename
    metas['directory'] = os.path.abspath(directory)

    metas['date'] = datetime.fromtimestamp(os.path.getmtime(filepath))

    return metas


META_FUNC = [
    getFileMeta,
    getExifMeta,
]


def getMetadata(filepath: str) -> List[Dict[str, Any]]:
    metas = dict()

    for getMeta in META_FUNC:
        metas.update(getMeta(filepath))

    metas['date_added'] = datetime.now()

    return metas
        
