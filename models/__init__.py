#!/usr/bin/python3
"""Create a unique storage instance for your application"""
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")
# check envirn var to determine storage method
if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:  # file storage selected
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
