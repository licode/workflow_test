#!/usr/bin/env python
''' 
Created on July 12, 2013, last modified on July 19, 2013
@author: Cheng Chang (cheng.chang.ece@gmail.com)
         Computer Science Group, Computational Science Center
         Brookhaven National Laboratory
Modified by Wei Xu on July 20, 2013
'''

import sys
import scipy
import scipy.io
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
import Image
from time import time
from scipy.optimize import minimize
from workflow.workflow_setting import result_path, home_path

def merge_LSF(filename):
    
    print 'Start Merging...'
    
    t0 = time()
    
    final_fraction = np.zeros((1024,1024,3))
    final_fval = np.zeros((1024,1024))
    
    local_path = home_path + 'Parallel_Packages/X8C/'
    for i in range(8*32): # 8*32 cores
        dict = scipy.io.loadmat(local_path+'sub_fitting/sub_final_Python.'+str(i))
        sub_final_fraction = dict['sub_final_fraction']
        sub_final_fval = dict['sub_final_fval']
        final_fraction[i*4:(i+1)*4, :, :] = sub_final_fraction
        final_fval[i*4:(i+1)*4, :] = sub_final_fval
    
    dict = {}
    dict['fraction_Python'] = final_fraction
    dict['fval_Python'] = final_fval

    scipy.io.savemat(result_path+'final_Python.mat', dict)
    out_img = Image.fromarray(np.uint8(final_fraction*255))
    out_img.save(result_path+filename)

    t1 = time()
    print t1 - t0
    print 'Done Merging.'

if __name__ == '__main__':
    filename = 'default.tif'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    merge_LSF(filename)
