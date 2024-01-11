#!/usr/bin/python3
"""
This module supplies a fabric script that configures a server
"""
from fabric.api import local, task, put, run, env
from datetime import datetime
import os.path import exists

env.user = "ubuntu"
env.hosts = ['18.234.192.15', '54.160.105.242']
env.key_filename = '~/.ssh/school'


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


@task
def do_deploy(archive_path):
    """distributes ana rchive to the servers"""
    if exists(archive_path) is False:
        return False
    try:
        dn = archive_path[9:-4]
        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{dn}/')
        run(f'tar -xzf /tmp/{dn}.tgz -C /data/web_static/releases/{dn}/')
        run(f'rm /tmp/{dn}.tgz')
        run(f'mv /data/web_static/releases/{dn}/web_static/* '
            f'/data/web_static/releases/{dn}/')
        run('rm -rf /data/web_static/releases/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{dn}/ /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception:
        return False
