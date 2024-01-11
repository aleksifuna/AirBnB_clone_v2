#!/usr/bin/python3
"""
This module supplies a fabric script that generates a .tgz archive
"""
from fabric.api import local, task, put, run, env
from datetime import datetime
import os

env.user = "ubuntu"
env.hosts = ['18.234.192.15', '54.160.105.242']


@task
def do_pack():
    """packs web_static folder to .tgz archive"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        arch_name = 'web_static_' + timestamp + '.tgz'
        local('mkdir -p versions')
        local('tar -cvzf versions/' + arch_name + ' web_static')
        return 'versions/' + arch_name
    except Exception:
        return None
