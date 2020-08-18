#!/usr/bin/python3
"""Creates and distributes an archive to
your web servers, using the function deploy"""

from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy


def deploy():
    """Deploy web_static content"""
    created_archive = do_pack()
    if created_archive is None:
        return False
    result = do_deploy('./versions/web_static_2020817232536.tgz')
    return result
