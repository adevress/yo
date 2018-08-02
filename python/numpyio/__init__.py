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


def load(filename, *args, **kwargs):
    try:
        return numpy.load(filename, *args, **kwargs)
    except ValueError as e:
        raise IOError("IOError: while reading %s because %s" % (filename, str(e)))

