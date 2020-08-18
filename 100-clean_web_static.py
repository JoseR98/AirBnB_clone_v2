#!/usr/bin/python3
"""Deletes out-of-date archives"""

import os
import glob
from fabric.api import run, env, local


env.hosts = ['35.243.225.26', '34.75.87.53']


def do_clean(number=0):
    """Delete versions of compressed files ready for deployment"""
    # Get all files from versions folder

    files = glob.glob('./versions/*')
    server_dir = '/data/web_static/releases'

    files.sort(key=os.path.getctime)
    count = 1
    for f in files:
        if count > number:
            f_name = f.split('/')[2].split('.')[0]
            local("sudo rm -rf {}.tgz".format(f_name))
            run("sudo rm -rf " + server_dir + "/{}".format(f_name))
        else:
            count += 1
