#!/usr/bin/python3
"""..."""
from datetime import datetime
from fabric.api import *
import shlex
import os


env.hosts = ['54.236.41.101', '34.224.6.181']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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


def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.replace('/', ' ')
        name = shlex.split(name)
        name = name[-1]

        s_name = name.replace('.', ' ')
        s_name = shlex.split(s_name)
        s_name = s_name[0]

        # parse name
        put(archive_path, "/tmp/")
        new_path = "/data/web_static/releases/{}/".format(s_name)
        tmp_path = "/tmp/{}".format(name)

        run("sudo mkdir -p {}".format(new_path))
        run("sudo tar -xzf {} -C {}".format(tmp_path, new_path))

        # remove archive
        run("sudo rm {}".format(tmp_path))

        # move contents in to host web_static
        run('sudo rsync -a {}web_static/* {}'.format(new_path, new_path))
        run('sudo rm -rf {}web_static/*'.format(new_path))
        # remove extranous web_static dir
        run("sudo rm -rf {}web_static".format(new_path))

        # remove previous symbolic link
        run("sudo rm -rf /data/web_static/current")

        # create new symbolic link
        run("sudo ln -s {} /data/web_static/current".format(new_path))
        print("New version deployed!")
        return True

    except:
        return False


def deploy():
    """..."""
    value = do_pack()
    if not value:
        return False
    return do_deploy(value)
