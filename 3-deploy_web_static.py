#!/usr/bin/python3
"""
This module supplies a fabric script that generates a .tgz archive
"""
from fabric.api import local, task, put, run, env, runs_once
from datetime import datetime
import os

env.user = "ubuntu"
env.hosts = ['18.234.192.15', '54.160.105.242']
env.key_filename = '~/.ssh/school'


@runs_once
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


def do_deploy(archive_path):
    """distributes an archive to the servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        dn = archive_path.split('/')[1].split('.')[0]
        put(archive_path, '/tmp/' + dn + '.tgz', use_sudo=True)
        run(f'mkdir -p /data/web_static/releases/{dn}/')
        run(f'tar -xzf /tmp/{dn}.tgz -C /data/web_static/releases/{dn}/')
        run(f'rm /tmp/{dn}.tgz')
        run(f'mv /data/web_static/releases/{dn}/web_static/* '
            f'/data/web_static/releases/{dn}/')
        run(f'rm -rf /data/web_static/releases/{dn}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{dn}/ /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to webservers"""
    archive = do_pack()
    if archive:
        return do_deploy(archive)
    return False
