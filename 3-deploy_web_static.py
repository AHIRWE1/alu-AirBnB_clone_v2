#!/usr/bin/env python3
"""
Fabric script to create and deploy an archive to web servers.
"""

from fabric.api import env
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy

# Replace with your actual web server IPs
env.hosts = ['3.95.225.29', '44.203.123.70']
env.user = 'ubuntu'


def deploy():
    """
    Creates a .tgz archive from web_static and deploys it to web servers.

    Returns:
        bool: True if all operations succeeded, False otherwise
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    result = do_deploy(archive_path)
    return result