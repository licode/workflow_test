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

def con_func(x, m_ref1, m_ref2, m_ref3, s_imgEstack):
    ''' This is the (least square) cost function to be minimized in the constrained optimization algorithm
    '''
    matrix_ref_com = x[0] * m_ref1 + x[1] * m_ref2 + x[2] * m_ref3
    sqr = (s_imgEstack - matrix_ref_com) * (s_imgEstack - matrix_ref_com)
    R_ref = np.sum(sqr)
    return R_ref

def preprocess():

    print 'Start preprocessing...'
    t0 = time()

    th = 20  # Edge jump threshold; only consider the points that have different value for below and above absorption edge
    step = 5  # The chemical composition resolution as % --> this is unnecessary, can use least square instead

    # No 5 after 1st half cycle
    imgpath = '/kbase/home/wxu/WorkflowPrototype/Parallel_Packages/X8C/CuONo5_XANES_1stCylEnd_Sam_export_tiff/'  # Image path
    bkgpath = '/kbase/home/wxu/WorkflowPrototype/Parallel_Packages/X8C/CuONo5_XANES_1stCylEnd_Bkg_export_tiff/'  # Background path
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

    # Spectrum fitting pixel by pixel

    # Initializing the reference matrix
    matrix_ref1 = np.copy(ln_imgEstack)
    matrix_ref2 = np.copy(ln_imgEstack)
    matrix_ref3 = np.copy(ln_imgEstack)

    # Read in the spectrum pre-saved for the three standards by running the script "XANES_No5Analysis_v02.py"
    mat = scipy.io.loadmat('Cu_CuO_Cu2O_E8960_9040eV_natlog.mat')
    scale_spec_ref1 = mat['scale_spec_ref1']
    scale_spec_ref2 = mat['scale_spec_ref2']
    scale_spec_ref3 = mat['scale_spec_ref3']

    for i in range(numE):
        matrix_ref1[:, :, i] = scale_spec_ref1[0][i]
        matrix_ref2[:, :, i] = scale_spec_ref2[0][i]
        matrix_ref3[:, :, i] = scale_spec_ref3[0][i]
    
    # This part scales the spectrum from the image data;
    scale_0 = np.mean(ln_imgEstack[:, :, 0:5], axis=2)
    scale_1 = np.mean(ln_imgEstack[:, :, -5:], axis=2)

    # Expand the scale_0 and scale_1
    expand_scale_0 = np.copy(ln_imgEstack)
    expand_scale_1 = np.copy(ln_imgEstack)
    
    for i in range(numE):
        expand_scale_0[:, :, i] = scale_0
        expand_scale_1[:, :, i] = scale_1

    # Scale the image energy stack
    scale_imgEstack = (ln_imgEstack - expand_scale_0) / (expand_scale_1 - expand_scale_0)
    sqdata = scale_imgEstack * scale_imgEstack
    sum_sqdata =  np.sum(sqdata, axis=2)

    t2 = time()
    print 'Time spent: ', t2 - t0

    # store results to mat file
    for i in range(128): # 4*32 cores, each handle 8 out-loop
        sub_matrix_ref1 = matrix_ref1[i*8:(i+1)*8, :, :]
        sub_matrix_ref2 = matrix_ref2[i*8:(i+1)*8, :, :]
        sub_matrix_ref3 = matrix_ref3[i*8:(i+1)*8, :, :]
        sub_scale_imgEstack = scale_imgEstack[i*8:(i+1)*8, :, :]
        sub_sum_sqdata = sum_sqdata[i*8:(i+1)*8, :]
        dict = {}
        dict['matrix_ref1'] = sub_matrix_ref1
        dict['matrix_ref2'] = sub_matrix_ref2
        dict['matrix_ref3'] = sub_matrix_ref3
        dict['scale_imgEstack'] = sub_scale_imgEstack
        dict['sub_sum_sqdata'] = sub_sum_sqdata
        scipy.io.savemat('standard_spectrum/standard.'+str(i), dict)

    print 'Finish data writing.'

##########################################################################################
######################## This part runs the least square fitting #########################
##########################################################################################
def LSF():
    print 'Start LSF...'
    t0 = time()

    for i in range(128):
        t_core_s = time()
        # sub final results
        sub_final_fraction = np.zeros((8,1024,3))
        sub_final_fval = np.zeros((8,1024))
        # con_min parameters
        cons = ({'type' : 'eq', \
                'fun' : lambda x: 1 - x[0] - x[1] - x[2]})
        bnds = ((0, 1), (0, 1), (0, 1))
        # load data for this core
        dict = scipy.io.loadmat('standard_spectrum/standard.'+str(i))
        sub_matrix_ref1 = dict['matrix_ref1']
        sub_matrix_ref2 = dict['matrix_ref2']
        sub_matrix_ref3 = dict['matrix_ref3']
        sub_scale_imgEstack = dict['scale_imgEstack']
        sub_sum_sqdata = dict['sub_sum_sqdata']
        # start the real computation
        for ii in range(8):
            for j in range(1024):
                res = minimize(con_func, [0.35, 0.35, 0.3], \
                               args=(sub_matrix_ref1[ii, j, :], \
                                     sub_matrix_ref2[ii, j, :], \
                                     sub_matrix_ref3[ii, j, :], \
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
        scipy.io.savemat('sub_fitting/sub_final_Python.'+str(i), dict)

        t_core_e = time()
        # done with one core
        print i,': ',t_core_e - t_core_s

    t1 = time()
    print t1 - t0

def merge_LSF():
    
    print 'Start Merging...'
    
    t0 = time()
    
    final_fraction = np.zeros((1024,1024,3))
    final_fval = np.zeros((1024,1024))
    
    for i in range(128):
        dict = scipy.io.loadmat('sub_fitting/sub_final_Python.'+str(i))
        sub_final_fraction = dict['sub_final_fraction']
        sub_final_fval = dict['sub_final_fval']
        final_fraction[i*8:(i+1)*8, :, :] = sub_final_fraction
        final_fval[i*8:(i+1)*8, :] = sub_final_fval
    
    dict = {}
    dict['fraction_Python'] = final_fraction
    dict['fval_Python'] = final_fval

    scipy.io.savemat('final_Python.mat', dict)

    t1 = time()
    print t1 - t0


if __name__ == '__main__':
    t0 = time()    
    preprocess()
    LSF()
    merge_LSF()
    t1 = time()
    print 'final time:', t1-t0
