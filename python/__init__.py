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

def copy(src, dst, *, follow_symlinks=False):
    assert (not follow_symlinks), "Yo does not support following symlinks"
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    shutil.copymode(src, dst, follow_symlinks=False)

def copy2(src, dst, *, follow_symlinks=False):
   assert(not follow_symlinks), "Yo does not support following symlinks"
   if os.path.isdir(dst):
       dst = os.path.join(dst, os.path.basename(src))
   copyfile(src, dst)
   shutil.copystat(src, dst, follow_symlinks=False)

def move(src, dst):
    return shutil.move(src, dst, copy_function=copy2)

def copytree(src, dst, ignore_dangling_symlinks=False):
    return shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=ignore_dangling_symlinks)


__version__ = "1.4"

