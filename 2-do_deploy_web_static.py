#!/usr/bin/env python3
"""
Fabric script to deploy an archive to web servers.
"""

from fabric.api import env, put, run
import os

# Replace these IPs with your actual web server IPs
env.hosts = ['3.95.225.29', '44.203.123.70']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive file

    Returns:
        bool: True if all operations succeeded, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    # Extract filename without path and extension
    file_name = os.path.basename(archive_path)
    name_no_ext = os.path.splitext(file_name)[0]
    release_path = f"/data/web_static/releases/{name_no_ext}/"

    try:
        # Upload archive to /tmp/
        put(archive_path, f"/tmp/{file_name}")

        # Create release folder
        run(f"mkdir -p {release_path}")

        # Uncompress archive into release folder
        run(f"tar -xzf /tmp/{file_name} -C {release_path}")

        # Delete the archive from /tmp/
        run(f"rm /tmp/{file_name}")

        # Move contents out of the web_static folder
        run(f"mv {release_path}web_static/* {release_path}")

        # Delete now empty web_static folder
        run(f"rm -rf {release_path}web_static")

        # Delete current symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False