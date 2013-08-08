#! usr/bin/env python

"""
    Collect slices to form the volume data and save in hdf5 file
    @author: Wei Xu
    @affilication: CSC @ BNL
    @date created: Aug. 6, 2013
    @date last modified: Aug. 6, 2013
"""

import sys
import numpy as np
import scipy.io
from time import time
from workflow.workflow_setting import data_path, home_path
import h5py

def collect3d(outfilepath):
    """
        Collect a set of 2D slices to form a volume
    """
    local_path = home_path + 'Parallel_Packages/Tomo/'
    
    file = h5py.File(outfilepath, 'w') #volume stack
    volume = file.create_dataset('volume', (1026,1026,20), dtype = 'f')

    for i in range(20):
        #t0 = time()
        name = 'slice_'+str(i)
        dict = scipy.io.loadmat(local_path+'sub_tomo/'+name)
        slice = dict['slice']
        volume[:,:,i] = slice
        #t1 = time()
        #print i, ':', t1-t0

    file.close() #hdf5 file

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        raise "No enough input parameters!"

    collect3d(sys.argv[1])
