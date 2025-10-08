#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static.
    
    Returns:
        str: The archive path if successfully generated, else None.
    """
    # Create versions folder if it doesn't exist
    if not os.path.isdir("versions"):
        os.makedirs("versions")

    # Format timestamp for the archive filename
    now = datetime.now()
    archive_name = "versions/web_static_{}{:02}{:02}{:02}{:02}{:02}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )

    try:
        # Create the archive
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        print("Error: {}".format(e))
        return None