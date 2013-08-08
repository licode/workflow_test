#!/usr/bin/env python

'''
Created on July 12, 2013, last modified on July 19, 2013
@author: Cheng Chang (cheng.chang.ece@gmail.com)
         Computer Science Group, Computational Science Center
         Brookhaven National Laboratory
Modified by Wei Xu on July 20, 2013
'''

import scipy
import scipy.io
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from time import time
from scipy.optimize import minimize
from mpi4py import MPI

def con_func(x, m_ref1, m_ref2, m_ref3, s_imgEstack):
    ''' This is the (least square) cost function to be minimized in the constrained optimization algorithm
        '''
    matrix_ref_com = x[0] * m_ref1 + x[1] * m_ref2 + x[2] * m_ref3
    sqr = (s_imgEstack - matrix_ref_com) * (s_imgEstack - matrix_ref_com)
    R_ref = np.sum(sqr)
    return R_ref

def spectroscopy():

#    print 'Start preprocessing'
    t0 = time()

    th = 20  # Edge jump threshold; only consider the points that have different value for below and above absorption edge
    step = 5  # The chemical composition resolution as % --> this is unnecessary, can use least square instead

    # No 5 after 1st half cycle
    machine_local = '/Users/weixu/Desktop/BNL/Projects/Karen/'
    machine_cluster = '/kbase/home/wxu/WorkflowPrototype/Parallel_Packages/X8C/'
    flag = False
    if flag:
        home_path = machine_local
    else:
        home_path = machine_cluster

    imgpath = home_path+'CuONo5_XANES_1stCylEnd_Sam_export_tiff/'  # Image path
    bkgpath = home_path+'CuONo5_XANES_1stCylEnd_Bkg_export_tiff/'  # Background path
    imgprefix = 'JJCuO_No5_2FirstCycleEnd_sam_'  # Image file name prefix before the energy
    bkgprefix = 'JJCuO_No5_2FirstCycleEnd_bkg_'  # Background file name prefix before the energy

    Ei = 8960  # Initial energy of scan
    Ee = 9040  # End energy of scan
    bin = 2  # Raw data binning
    ROI = 1  # Must be odd number; determine how many pixel x pixel are binned when doing fitting
    Estep = 2  # Energy step size for energy scan
    numE = (Ee-Ei) / Estep + 1  # number of energies

    # On point of interest just for checking the spectrum; not very important
    pointx = 454
    pointy = 322

    img_num = (Ee-Ei) / Estep + 1  # Total number of images
    i = 0
    # Define the size of the image stack with energy as the 3rd dimension, detector size: 2048x2048
    imgEstack = np.arange(img_num*(2048/bin)**2, dtype='d').reshape(2048/bin, 2048/bin, img_num)
    ln_imgEstack = np.arange(img_num*(2048/bin)**2, dtype='d').reshape(2048/bin, 2048/bin, img_num)

    for E in range(Ei, Ee+2, Estep):
    
        E_text = '%04d' % E
        
        # Read image data
        imgfn = imgpath + imgprefix + E_text + '.tiff'
        img = plt.imread(imgfn) * 1.0  # convert img to float 64 (double) type by multiplying it with 1.0
    
        # Read background data
        bkgfn = bkgpath + bkgprefix + E_text + '.tiff'
        bkg = plt.imread(bkgfn) * 1.0
    
        scaleimg = img / bkg  #scaleimg is the same as that in MATLAB
        imgEstack[:, :, i] = np.uint8(scaleimg*255+0.5)  # Add 0.5 to make up for the difference of uint8() between M and P
        ln_imgEstack[:, :, i] = -np.log(scaleimg)
        i = i + 1
    
    # Leave out the display part at this moment
    ########################################################################

    # Deal with the pixels that have edge jump
    prepostEdgeDiff = imgEstack[:, :, 0] - imgEstack[:, :, -1]  # Calculate the difference of below/above edge
    filter = np.greater_equal(prepostEdgeDiff, th)
    
    # Release the memory space
    del imgEstack

    # Spectrum fitting pixel by pixel

    # Initializing the reference matrix
    matrix_ref1 = np.zeros(ln_imgEstack.shape)
    matrix_ref2 = np.zeros(ln_imgEstack.shape)
    matrix_ref3 = np.zeros(ln_imgEstack.shape)

    # Read in the spectrum pre-saved for the three standards by running the script "XANES_No5Analysis_v02.py"
    mat = scipy.io.loadmat('Cu_CuO_Cu2O_E8960_9040eV_natlog.mat')
    scale_spec_ref1 = mat['scale_spec_ref1']
    scale_spec_ref2 = mat['scale_spec_ref2']
    scale_spec_ref3 = mat['scale_spec_ref3']

    # This part scales the spectrum from the image data;
    scale_0 = np.mean(ln_imgEstack[:, :, 0:5], axis=2)
    scale_1 = np.mean(ln_imgEstack[:, :, -5:], axis=2)

    # Expand the scale_0 and scale_1
    expand_scale_0 = np.zeros(ln_imgEstack.shape)
    expand_scale_1 = np.zeros(ln_imgEstack.shape)
    
    for i in range(numE):
        expand_scale_0[:, :, i] = scale_0
        expand_scale_1[:, :, i] = scale_1

    # Scale the image energy stack
    scale_imgEstack = (ln_imgEstack - expand_scale_0) / (expand_scale_1 - expand_scale_0)
    sqdata = scale_imgEstack * scale_imgEstack
    sum_sqdata =  np.sum(sqdata, axis=2)

    del ln_imgEstack

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # store results to local variables
    sub_scale_imgEstack = []
    sub_sum_sqdata = []
    for i in [rank]: # 8*32 cores, each handle 4 out-loop
        sub_scale_imgEstack = scale_imgEstack[i*4:(i+1)*4, :, :]
        sub_sum_sqdata = sum_sqdata[i*4:(i+1)*4, :]

    del scale_imgEstack
    del sum_sqdata

 #   t2 = time()
 #   print 'Time spent: ', t2 - t0

#    print 'Finish preprocessing.'

############################################################
############################################################
###        LSF                                           ###
############################################################
############################################################

#    print 'Start LSF...'
#    t0 = time()

    for i in [rank]: #lazy writing
    #    t_core_s = time()
        # sub final results
        sub_final_fraction = np.zeros((4,1024,3))
        sub_final_fval = np.zeros((4,1024))
        # con_min parameters
        cons = ({'type' : 'eq', \
                'fun' : lambda x: 1 - x[0] - x[1] - x[2]})
        bnds = ((0, 1), (0, 1), (0, 1))

        # start the real computation
        for ii in range(4):
            for j in range(1024):
                res = minimize(con_func, [0.35, 0.35, 0.3], \
                               args=(scale_spec_ref1, \
                                     scale_spec_ref2, \
                                     scale_spec_ref3, \
                                     sub_scale_imgEstack[ii, j, :]), \
                               method='SLSQP', \
                               bounds=bnds, \
                               constraints=cons, \
                               options = {'ftol': 1e-6})
                sub_final_fraction[ii, j, 0] = res.x[0]
                sub_final_fraction[ii, j, 1] = res.x[1]
                sub_final_fraction[ii, j, 2] = res.x[2]
                sub_final_fval[ii, j] = res.fun / sub_sum_sqdata[ii, j]
        # save data for this core
        dict = {}
        dict['sub_final_fraction'] = sub_final_fraction
        dict['sub_final_fval'] = sub_final_fval
        scipy.io.savemat('sub_fitting/sub_final_Python.'+str(i), dict, oned_as='row')
    
     #   t_core_e = time()
        # done with one core
 #       print i,': ',t_core_e - t_core_s

#    print 'Done LSF'

#    t1 = time()
#    print t1 - t0

if __name__ == '__main__':
    t0 = time()    
    spectroscopy()
    t1 = time()
    #print t1 - t0
