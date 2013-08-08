#! usr/bin/env python
"""
    Filtered backprojection from phantom image
    """
import sys
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import Image
from time import time
from mpi4py import MPI
import parallel_beam as pb
from workflow.workflow_setting import data_path, home_path
import h5py

def recon2d(filepath):
    """
        Reconstruct a set of 2D slices
    """
    # Set up MPI environment
    local_path = home_path + 'Parallel_Packages/Tomo/'
    comm = MPI.COMM_WORLD
    nodeID = comm.Get_rank()
    total = comm.Get_size()
    slice_start = 0
    slice_end = 0
    
    file = h5py.File(filepath) #sinogram stack
    theta = file['/theta']
    size = len(file['/sinogram']) #number of slices
    
    # Compute starting and ending slices for this core
    label = size / total
    label_rest = size - label * total
    
    if nodeID < label_rest:
        slice_start = nodeID * (label + 1)
        slice_end = (nodeID + 1) * (label + 1) #doesn't count the last number
    else:
        slice_start = label_rest * (label + 1) + (nodeID - label_rest) * label
        slice_end = label_rest * (label + 1) + (nodeID - label_rest + 1) * label #range doesn't cound the last number

    for i in range(slice_start, slice_end):
        #t0 = time()
        name = 'slice_'+str(i)
        sinogram = file['/sinogram/'+name] #take one sinogram
        reconed_slice = pb.iradon(sinogram[...], theta[...])
        print 'recon done for', i
        dict = {}
        dict['slice'] = reconed_slice
        scipy.io.savemat(local_path+'sub_tomo/'+name, dict, oned_as='row')
        #t1 = time()
    
        #print i, ':', t1-t0
    
    temp_file.close()
    file.close() #hdf5 file

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        raise "No enough input parameters!"

    recon2d(sys.argv[1])

