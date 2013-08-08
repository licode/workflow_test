#! usr/bin/env python
"""
    Filtered backprojection from phantom image
    """
import sys
import numpy as np
import matplotlib.pyplot as plt
import Image
import parallel_beam as pb
from workflow.workflow_setting import data_path
import h5py
from time import time

def recon3d(filepath, outfilepath):
    
    file = h5py.File(filepath)
    
    outfile = h5py.File(outfilepath, 'w')
    
    theta = file['/theta']
    size = len(file['/sinogram'])
    
    volume = outfile.create_dataset('volume', (1026,1026,size), dtype = 'f')

    for i in range(size):
        #t0 = time()
        name = '/sinogram/slice_'+str(i)
        sinogram = file[name]
        reconed_slice = pb.iradon(sinogram[...], theta[...])
        volume[:,:,i] = reconed_slice
        #t1 = time()
    
        #print i, ':', t1-t0

    outfile.close()
    file.close()

if __name__ == '__main__':
    
    if (len(sys.argv) < 3):
        raise "No enough input parameters!"
    
    recon3d(sys.argv[1], sys.argv[2])

