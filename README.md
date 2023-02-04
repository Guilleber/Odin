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

## Disclaimer

This project is still in a work in progress state. I strongly advise against using it
on any not backed up data as it may contains bugs that could damage or erase your data.

## Installation

To use Odin, you first need to install MongoDB. To do so, please follow the instructions on the official [MongoDB website](https://www.mongodb.com/docs/manual/installation/).

Then simply install the package using pip as follows:

    python3 -m pip install git+https://github.com/Guilleber/Odin.git

## Usage

### Getting Started

Every time you want to use Odin, you first need to start the MongoDB server.

    odin start

You can then initialize a new collection.

    odin init [-c | --collection <collection-name>]

If no *collection-name* is provided, Odin will initialize a new collection with a default name.
This holds true for other commands as well and if you do not specify a *collection-name*,
the command will apply on the default collection.

### Adding, removing and finding files

You can add new files to the index using:

    odin add [-c | --collection <collection-name>] <path>...

where *path* can be a file, a directory and/or a regex. When a directory is provided,
Odin will index all the files in that directory including all subdirectories.

Indexed files can be removed using a MongoDB style query.

    odin rm [-c | --collection <collection-name>] <query>

Similarly to the rm command, one can print a set of documents matching a given query.

    odin find [-c | --collection <collection-name>] <query>

### File Manipulation

You can move files by using:

    odin mv [-c | --collection <collection-name>] [--on-exists (replace|rename)] <query> <destination>

This command will move all files matching *query* to the directory *destination*.

### Exemples

Add files to index

    odin add ~/Photos/Japan
    odin add /home/user/Photos/DSCF6421.RAF
    odin add ../Photos/*.JPG

Show all indexed jpeg files

    odin find '{"filename": {"$regex": ".JPG$"}}'

Remove all files in a directory from the index

    odin rm '{"directory": {"$regex": "^/home/user/Photos/Japan"}}'

Move all photos taken with an ISO of less than 500 to a specific directory

    odin mv '{"iso": {"$lte": 500}}' ./HighQuality
