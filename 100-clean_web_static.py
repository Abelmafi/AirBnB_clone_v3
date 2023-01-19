#!/usr/bin/python3
"""deletes out-of-date archives"""
from fabric.api import *


env.hosts = ['54.236.41.101', '34.224.6.181']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """deletes out-of-date archives"""

    _list = local("ls -1t versions", capture=True)
    _list = _list.split('\n')
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in _list[n:]:
        local('rm versions/' + i)

    _list1 = run("ls -1t /data/web_static/releases")
    _list1 = _list1.split('\r\n')
    for j in _list1[n:]:
        run("rm -rf /data/web_static/releases" + j)
