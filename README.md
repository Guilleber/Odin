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

To use Odin, you first need to install MongoDB. To do so, please follow the instructions on the official [MongoDB website](https://www.mongodb.com/docs/manual/installation/).

Then simply install the package using pip as follows:

    python3 -m pip install git+https://github.com/Guilleber/Odin.git

## Usage

### Getting Started

Every time you want to use Odin, you first need to start the MongoDB server.

    odin start

You can then initialize a new collection.

    odin init [--collection <collection-name>]

If no <collection-name> is provided, Odin will initialize a new collection with a default name.
This holds true for other commands as well and if you do not specify a <collection-name>,
the command will apply on the default collection.

### Adding, removing and finding files

You can add new files to the index using:

    odin add [--collection <collection-name>] <path>...

where <path> can be a file, a directory and/or a regex. When a directory is provided,
Odin will index all the files in that directory including all subdirectories.

Indexed files can be removed using a MongoDB style query.

    odin rm [--collection <collection-name>] <query>

Similarly to the rm command, one can print a set of documents matching a given query.

    odin find [--collection <collection-name>] <query>
