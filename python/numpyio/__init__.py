# -*- coding: utf-8 -*-
###
##    yo, parallel I/O utilities
##    Copyright (C) 2018 Adrien Devresse
##
##  This Source Code Form is subject to the terms of the Mozilla Public
##  License, v. 2.0. If a copy of the MPL was not distributed with this
##  file, You can obtain one at http://mozilla.org/MPL/2.0/.
##

import numpy
import io

import yo


def save(filename, arr, *args, **kwargs):
    filename = str(filename)
    if not filename.endswith(".npy"):
        filename += ".npy"
    with open(filename, 'wb') as f:
        numpy.save(f, arr, *args, **kwargs)
        # a trick here
        # we enforce flush explicitely here
        # Many PFS have a relaxed POSIX model
        # and do not insure content consistency between clients excepted
        # in case of explicit flush
        f.flush()


def savez_compressed(filename, *args, **kwargs):
    filename = str(filename)
    if not filename.endswith(".npz"):
        filename += ".npz"
    with open(filename, 'wb') as f:
        numpy.savez_compressed(f, *args, **kwargs)
        # a trick here
        # we enforce flush explicitely here
        # Many PFS have a relaxed POSIX model
        # and do not insure content consistency between clients excepted
        # in case of explicit flush
        f.flush()


def load(filename, *args, **kwargs):
    try:
        if kwargs.get("mmap_mode", None) != None:
            # if the user want memory mapping, give him memory mapping
            return numpy.load(filename, *args, **kwargs)
        
        opts = yo.options()
        with io.FileIO(filename) as raw_file:
            with io.BufferedReader(raw_file, buffer_size=opts.get_block_size()) as buffer_io:
                return numpy.load(buffer_io, *args, **kwargs)
        
    except ValueError as e:
        raise IOError("IOError: while reading %s because %s" % (filename, str(e)))

