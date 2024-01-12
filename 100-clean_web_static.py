#!/usr/bin/python3
"""
Fabfile that deletes out of date archives.
"""
import os
from fabric.api import *

env.user = "ubuntu"
env.key_filename = '~/.ssh/school'
env.hosts = ['18.234.192.15', '54.160.105.242']


def do_clean(number=0):
    """
    Deletes out of date archives"
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir('versions'))
    [archives.pop() for i in range(number)]
    with lcd('versions'):
        [local(f'rm ./{archive}') for archive in archives]

    with cd('/data/web_static/releases'):
        archives = run('ls -tr').split()
        archives = [a for a in archives if 'web_static_' in a]
        [archives.pop() for i in range(number)]
        [run(f'rm -rf ./{archive}') for archive in archives]
