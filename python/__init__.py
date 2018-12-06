# -*- coding: utf-8 -*-
###
##    yo, parallel I/O utilities
##    Copyright (C) 2018 Adrien Devresse
##
##  This Source Code Form is subject to the terms of the Mozilla Public
##  License, v. 2.0. If a copy of the MPL was not distributed with this
##  file, You can obtain one at http://mozilla.org/MPL/2.0/.
##


from . _yo import (copyfile, options)
import shutil
'''
    import copyfile
'''
'''
    define a set of filesystem operations mimicking shutil, reusing the logic.
'''

# from shutil
def _samefile(src, dst):
    # Macintosh, Unix.
    if isinstance(src, os.DirEntry) and hasattr(os.path, 'samestat'):
        try:
            return os.path.samestat(src.stat(), os.stat(dst))
        except OSError:
            return False

    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))


def _copyfile(src, dst):
    if _samefile(src, dst):
        raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))
    else:
        copyfile(src,dst)


def copy(src, dst, follow_symlinks=False):
    assert (not follow_symlinks), "Yo does not support following symlinks"
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    _copyfile(src, dst)
    shutil.copymode(src, dst, follow_symlinks=False)
    return dst


def copy2(src, dst, follow_symlinks=False):
   assert(not follow_symlinks), "Yo does not support following symlinks"
   if os.path.isdir(dst):
       dst = os.path.join(dst, os.path.basename(src))
   _copyfile(src, dst)
   shutil.copystat(src, dst, follow_symlinks=False)
   return dst


def move(src, dst):
    return shutil.move(src, dst, copy_function=copy2)


def copytree(src, dst, ignore_dangling_symlinks=False):
    return shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=ignore_dangling_symlinks)


__version__ = "1.4"

