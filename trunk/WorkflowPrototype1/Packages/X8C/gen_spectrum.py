#!/usr/bin/env python
''' 
Created on July 14, 2013, last modified on July 16, 2013
@author: Cheng Chang (cheng.chang.ece@gmail.com)
         Computer Science Group, Computational Science Center
         Brookhaven National Laboratory
Modified by Wei Xu on July 20, 2013
'''

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


def XANES_functv02(imgpath, bkgpath, imgprefix, bkgprefix, Ei, Ee, Estep, bin, pointx, pointy, ROI):
    ''' This is a function
    '''
    img_num = (Ee-Ei) / Estep + 1  #total number of images
    i = 0
    ln_imgEstack = np.zeros(img_num*(2048/bin)*(2048/bin)).reshape(2048/bin, 2048/bin, img_num)
    
    # Read the file
    for E in range(Ei, Ee+2, Estep):
    
        E_text = '%04d' % E
        
        # Read image data
        imgfn = imgpath + imgprefix + E_text + '.tiff'
        img = plt.imread(imgfn) * 1.0  # convert img to float 64 (double) type by multiplying it with 1.0
        
        # Read background data
        bkgfn = bkgpath + bkgprefix + E_text + '.tiff'
        bkg = plt.imread(bkgfn) * 1.0
        
        ln_imgEstack[:, :, i] = -np.log(img/bkg)
        i = i + 1

    Eaxis  = range(Ei, Ee+2, Estep)
    
    # Handle ROI
    if ROI > 1:
        ROI_hsize = (ROI-1) / 2
        
        a = 0
        point_spectrum = np.zeros(img_num*ROI*ROI).reshape(img_num, ROI*ROI)
    
        for j in range(-ROI_hsize, ROI_hsize+1):
            for k in range (-ROI_hsize, ROI_hsize+1):
                point_spectrum[:, a] = np.squeeze(ln_imgEstack[pointy+j-1, pointx+k-1, :])
                a = a + 1
    
        spectrum = np.mean(point_spectrum, axis=1)
    else:
        spectrum = np.squeeze(in_imgEstack[pointy-1, pointx-1, :])
    
    # Scale the spectrum
    scale_0 = np.mean(spectrum[0:5])
    scale_1 = np.mean(spectrum[-5:])
    
    scale_spec = (spectrum-scale_0) / (scale_1-scale_0)
    return Eaxis, scale_spec


Ei = 8960
Ee = 9040
bin = 2
ROI = 5
Estep = 2
pointx = 558
pointy = 590

imgpath = '/Users/weixu/Desktop/BNL/Projects/Karen/CuONo5_XANES_1stCylEnd_Sam_export_tiff/'
bkgpath = '/Users/weixu/Desktop/BNL/Projects/Karen/CuONo5_XANES_1stCylEnd_Bkg_export_tiff/'
imgprefix = 'JJCuO_No5_2FirstCycleEnd_sam_'  #image file name prefix before the energy
bkgprefix = 'JJCuO_No5_2FirstCycleEnd_bkg_'  #background file name prefix before the energy
Eaxis, scale_spec = XANES_functv02(imgpath, bkgpath, imgprefix, bkgprefix, Ei, Ee, Estep, bin, pointx, pointy, ROI)

path = '/Users/weixu/Desktop/BNL/Projects/Karen/Cu_export_tiff/'
imgprefix = 'Cu'
bkgprefix = 'Cubkg'
ref1_name = imgprefix
pointx = 520
pointy = 526
ROI = 33
imgpath = path
bkgpath = path
Eaxis, scale_spec_ref1 = XANES_functv02(imgpath, bkgpath, imgprefix, bkgprefix, Ei, Ee, Estep, bin, pointx, pointy, ROI)

path = '/Users/weixu/Desktop/BNL/Projects/Karen/Cu2O_export_tiff/'
imgprefix = 'Cu2O'
bkgprefix = 'Cu2Obkg'
ref2_name = imgprefix
imgpath = path
bkgpath = path
Eaxis, scale_spec_ref2 = XANES_functv02(imgpath, bkgpath, imgprefix, bkgprefix, Ei, Ee, Estep, bin, pointx, pointy, ROI)

path = '/Users/weixu/Desktop/BNL/Projects/Karen/CuO_export_tiff/'
imgprefix = 'CuO'
bkgprefix = 'CuObkg'
ref3_name = imgprefix
imgpath = path
bkgpath = path
Eaxis, scale_spec_ref3 = XANES_functv02(imgpath, bkgpath, imgprefix, bkgprefix, Ei, Ee, Estep, bin, pointx, pointy, ROI)

# Quick calculation of the R value for ref1-3 
# For this specific point of interest
sqdata = scale_spec * scale_spec
sqr1 = (scale_spec - scale_spec_ref1) * (scale_spec - scale_spec_ref1)
sqr2 = (scale_spec - scale_spec_ref2) * (scale_spec - scale_spec_ref2)
sqr3 = (scale_spec - scale_spec_ref3) * (scale_spec - scale_spec_ref3)

R_ref1 = np.sum(sqr1[:]) / np.sum(sqdata[:])
R_ref2 = np.sum(sqr2[:]) / np.sum(sqdata[:])
R_ref3 = np.sum(sqr3[:]) / np.sum(sqdata[:])

dict = {}
dict['scale_spec_ref1'] = scale_spec_ref1
dict['scale_spec_ref2'] = scale_spec_ref2
dict['scale_spec_ref3'] = scale_spec_ref3
dict['ref1_name'] = ref1_name
dict['ref2_name'] = ref2_name
dict['ref3_name'] = ref3_name
scipy.io.savemat('Cu_CuO_Cu2O_E8960_9040eV_natlog.mat', dict, oned_as='row')