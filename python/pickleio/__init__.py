# -*- coding: utf-8 -*-
###
##    yo, parallel I/O utilities
##    Copyright (C) 2018 Adrien Devresse
##
##  This Source Code Form is subject to the terms of the Mozilla Public
##  License, v. 2.0. If a copy of the MPL was not distributed with this
##  file, You can obtain one at http://mozilla.org/MPL/2.0/.
##




import sys
import io

#  pickle / cPickle for python 2
if sys.version_info < (3,0):
    import cPickle as pickle
    def is_string(x):
        return type(x) in [str, unicode]
else:
    import pickle
    def is_string(x):
        return type(x) == str



import yo


def dump(obj, filename, *args, **kwargs):
    assert is_string(filename)

    opts = yo.options()

    with io.FileIO(filename, "w") as raw_file:
        with io.BufferedWriter(raw_file, buffer_size=opts.get_block_size()) as buffer_io:
            res = pickle.dump(obj, buffer_io, *args, **kwargs)
            buffer_io.flush()
            raw_file.flush()
    return res


def load(filename, *args, **kwargs):
    try:
        opts = yo.options()
        with io.FileIO(filename, "r") as raw_file:
            with io.BufferedReader(raw_file, buffer_size=opts.get_block_size()) as buffer_io:
                return pickle.load(buffer_io, *args, **kwargs)

    except ValueError as e:
        raise IOError("IOError: while reading %s because %s" % (filename, str(e)))
