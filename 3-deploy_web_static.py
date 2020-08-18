#!/usr/bin/python3
"""Creates and distributes an archive to
your web servers, using the function deploy"""

from os import path
from fabric.api import run, put, env, local
from datetime import datetime


def do_pack():
    """Compress web static content"""
    d = datetime.now()
    local("mkdir -p versions")
    file_name = 'versions/web_static_{}{}{}{}{}{}.tgz\
'.format(d.year, d.month, d.day, d.hour, d.minute, d.second)
    status = local("tar -cvzf" + file_name + " ./web_static/", capture=True)
    if status.succeeded:
        return file_name
    return None

env.hosts = ['35.243.225.26', '34.75.87.53']


def do_deploy(archive_path):
    """Deploy web_static content in servers"""
    if path.exists(archive_path):

        # File name without .tgz
        file_ext = archive_path.split('/')[1]
        file_alone = file_ext.split(".")[0]
        curr_release = "/data/web_static/releases/" + file_alone + '/'

        result = True

        # Deploy compressed file to the server /tmp/ directory
        upload = put(archive_path, "/tmp/")
        if upload.failed:
            result = False

        # Make dir to store the release
        dir_release = run("sudo mkdir -p " + curr_release)
        if dir_release.failed:
            result = False

        # Uncompress file inside the folder created
        uncompress = run("sudo tar -xzf " + "/tmp/\
" + file_ext + " -C " + curr_release)
        if uncompress.failed:
            result = False

        # Move all files from web_static to folder release
        move_info = run("sudo mv " + curr_release + "\
web_static/* " + curr_release)
        if move_info.failed:
            result = False

        # Remove empty web_static directory
        rm_empty = run("sudo rm -rf " + curr_release + "\
web_static/")
        if rm_empty.failed:
            result = False

        # Remove symbolic link current
        rm_link = run("sudo rm -rf /data/\
web_static/current")
        if rm_link.failed:
            result = False

        # Make new symbolic link
        new_link = run("sudo ln -s " + curr_release + " /data/\
web_static/current")
        if new_link.failed:
            result = False

        if result:
            return True
        else:
            return False
    else:
        return False

def deploy():
    """Deploy web_static content"""
    created_archive = do_pack()
    if created_archive is None:
        return False
    result = do_deploy(archive_path)
    return result
