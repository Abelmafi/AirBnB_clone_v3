#!/usr/bin/python3
"""Compress the web_static code file into new directory"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """ This function generates a .tgz archive from the contents of the
    web_static folder of your AirBnB Clone repo"""
    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_" + now + ".tgz"

    local("mkdir -p versions/")
    download = local("tar -cvzf {} web_static/".format(archive_path))
    if download.succeeded:
        return (archive_path)
    return (None)
