# ODIN Command Line Indexing Tool

Odin creates an index of documents on your disk using a local MongoDB database.
Files and directories can be added to the index via a simple command line interface and
Odin automatically extracts metadata information about all the indexed files
(as this tool is intended in the first place for photos, Odin will in particular
extract EXIF metadata containing information such as the hardware used to take the photo
and the GPS location of the image).

The indexed files can then be listed and manipulated using MongoDB style queries.
The possible operations include moving or copying file that match a specific query
to a destination directory.

## Installation
