#!/usr/bin/python3
"""Distributes an archive to your web servers,
using the function do_deploy"""

from os import path
from fabric.api import run, put, env
from datetime import datetime


env.hosts = ['35.243.225.26', '34.75.87.53']

def do_deploy(archive_path):
    """Deploy web_static content in servers"""
    if path.exists(archive_path):
        
        # File name without .tgz
        file_ext = archive_path.split('/')[1]
        file_alone = file_ext.split(".")[0]
        curr_release = "/data/web_static/releases/" + file_alone + '/'

        result = True

        upload = put(archive_path, "/tmp/")
        if upload.failed:
            result = False
        dir_release = run("sudo mkdir -p " + curr_release)
        if dir_release.failed:
            result = False
        uncompress = run("sudo tar -xzf " + "/tmp/\
" + file_ext + " -C " + curr_release)
        if uncompress.failed:
            result = False
        move_info = run("sudo mv " + curr_release + "\
web_static/* " + curr_release)
        if move_info.failed:
            result = False
        rm_empty = run("sudo rm -rf " + curr_release + "\
web_static/")
        if rm_empty.failed:
            result = False
        rm_link = run("sudo rm -rf /data/\
web_static/current")
        if rm_link.failed:
            result = False
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
