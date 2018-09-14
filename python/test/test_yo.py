# -*- coding: utf-8 -*-
###
##    yo, parallel I/O utilities
##    Copyright (C) 2018 Adrien Devresse
##
##  This Source Code Form is subject to the terms of the Mozilla Public
##  License, v. 2.0. If a copy of the MPL was not distributed with this
##  file, You can obtain one at http://mozilla.org/MPL/2.0/.
##




import unittest
import yo
import logging
import os
import traceback
import uuid
import sys
import tempfile

def create_junk(size): 
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(bytearray(os.urandom(size)))
    f.flush()
    return f.name

def copy_and_check(test, src, dst):
    import tempfile      
    info_src = os.stat(src)
    
    yo.copyfile(src, dst)
    info_dst = os.stat(dst)
    
    test.assertEqual(info_src.st_size, info_dst.st_size)
    
    
def digest_of_file(filename):
    import hashlib
    digest = hashlib.sha1()
    with open(filename, "rb") as f:
        digest.update(f.read())
    return digest.hexdigest()
            
    
    


class checkCopy(unittest.TestCase):
    def runTest(self):
        # copy a simple silly 0 byte file
        tmp_file = create_junk(0)
        tmp_file_dst = tempfile.NamedTemporaryFile()        
        copy_and_check(self, tmp_file, tmp_file_dst.name)
        self.assertEqual(digest_of_file(tmp_file), digest_of_file(tmp_file_dst.name))        
        
        # copy a simple silly 4MB byte file
        tmp_file = create_junk(2**22)
        tmp_file_dst = tempfile.NamedTemporaryFile()
        copy_and_check(self, tmp_file, tmp_file_dst.name)
        self.assertEqual(digest_of_file(tmp_file), digest_of_file(tmp_file_dst.name))
        
        
class checkNumpyIOBasic(unittest.TestCase):
    def runTest(self):
        import numpy as np
        import yo.numpyio as npio
        
        # save and load a simple matrix 1000x1000
        tmp_file = tempfile.NamedTemporaryFile()
        arr = np.random.rand(1000,1000)
        npio.save(tmp_file.name, arr)
        
        new_arr = npio.load(tmp_file.name + ".npy")
        self.assertTrue(np.array_equal(new_arr, arr))
        

class checkPickleIOBasic(unittest.TestCase):
    def runTest(self):
        import yo.pickleio as pio
        
        # save and load a simple matrix 1000x1000
        tmp_file = tempfile.NamedTemporaryFile()
        d = dict()
        for i in range(0, 1000):
            d["".format(i)] = i*i;
            
        pio.dump(d, tmp_file.name)
        
        new_dict = pio.load(tmp_file.name)
        
        self.assertEqual(len(d), len(new_dict))           
        for i in d:
            self.assertEqual(d[i], new_dict[i])
