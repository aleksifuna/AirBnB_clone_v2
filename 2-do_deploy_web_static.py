#!/usr/bin/python3
"""
This module supplies a fabric script that configures a server
"""
from fabric.api import local, task, put, run, env
import os

env.hosts = ['18.234.192.15', '54.160.105.242']


def do_deploy(archive_path):
    """distributes ana rchive to the servers"""
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
