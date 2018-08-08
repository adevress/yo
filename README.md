# YO

## SUMMARY

YO is a minimalist tool to maximize I/O throughput on top of Parallel File System (e.g GPFS, Lustre, BeeGFS, etc.... )

YO parallelise I/O for large sequential read/write pattern of few operations : file copy, sequential big I/O, numpy I/O )

YO is delivered with yocp: a parallel version of the cp tool


## USAGE

	yocp [src_file] [dst_file] 


## EXAMPLE

### YOCP example 
```bash

ls -lh $SHARED_HOME/test.big
-rwxr-xr-x 1 X X 3,0G  2 août  09:27 test.big



time cp $SHARED_HOME/test.big $SCRATCH/test.big2

real	0m33.622s
user	0m0.017s
sys	0m5.152s

time yocp $SHARED_HOME/test.big $SCRATCH/test.big3

real	0m22.094s
user	0m0.033s
sys	0m4.902s


```

### numpyio example 


```python

import yo.numpyio as npio
import numpy as np

z = np.zeros([3,3])

npio.save("/tmp/zero.npy", z)

## saved properly

r = npio.load("/tmp/zero.npy")

```


## ALGORITHM

YO uses simple multi-threaded parallel I/O using a multiple of the DFS block size

## DEPENDENCIES

- C++11 compatible compiler
- Boost > 1.41

Embedded component : [hadoken](https://github.com/adevress/hadoken)


## CONFIGURATION

### ENVIRONMENT VARIABLES

- YO_BLOCK_SIZE : size of the individual block to read in bytes

- YO_NUM_THREADS : number of working I/O threads




## LICENSE

Command line tools: GPLv3
Shared Library, Static library and python modules: MPL2

