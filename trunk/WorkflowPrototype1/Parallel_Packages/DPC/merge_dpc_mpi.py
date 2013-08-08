#! /usr/bin/env python2.7

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave
from scipy.optimize import fmin
from time import time
import Image

def merge(node_num = 1, namephi = 'phi.tif', namea = 'a.tif', namegx = 'gx.tif', namegy = 'gy.tif'):
    #print node_num
    row = 121
    column = 121
    dx = 0.1
    dy = 0.1
    file_path = '/kbase/home/wxu/WorkflowPrototype/Data/DPC/experiment/'
    home_path = '/kbase/home/wxu/WorkflowPrototype/Results/'
    a = np.zeros(row*column, dtype='d')
    gx = np.zeros(row*column, dtype='d')
    gy = np.zeros(row*column, dtype='d')

    i = 0
    for n in range(int(node_num)):
        filename = file_path + str(n) + '.txt'
        file = open(filename, 'rb')
        result = np.array(file.read().split(), dtype='d')
    
        for m in range(len(result)):
            if m % 3 == 0:
                a[i] = result[m]
            elif m % 3 == 1:
                gx[i] = result[m]
            elif m % 3 == 2:        
                gy[i] = result[m]
                i += 1

    a = a.reshape(row, column)
    imsave(home_path+namea, a)
    gx = gx.reshape(row, column)
    imsave(home_path+namegx, gx)
    gy = gy.reshape(row, column)
    imsave(home_path+namegy, gy)

    #-------------reconstruct the final phase image using gx and gy--------------------#
    w = 1 # Weighting parameter
    tx = np.fft.fftshift(np.fft.fft2(gx))
    ty = np.fft.fftshift(np.fft.fft2(gy))
    c = np.arange(row*column, dtype=complex).reshape(row, column)
    for i in range(row):
        for j in range(column):
            kappax = 2 * np.pi * (j+1-(np.floor(column/2.0)+1)) / (column*dx)
            kappay = 2 * np.pi * (i+1-(np.floor(row/2.0)+1)) / (row*dy)
            if kappax==0 and kappay==0:
                c[i, j] = 0
            else:
                cTemp = -1j * (kappax*tx[i][j]+w*kappay*ty[i][j]) / (kappax**2 + w*kappay**2)
                c[i, j] = cTemp
    c = np.fft.ifftshift(c)
    phi = np.fft.ifft2(c)
    phi = phi.real
    imsave(home_path+namephi, phi)
    #np.savetxt('phi.txt', phi)

if __name__ == '__main__':
#    if len(sys.argv) < 7:
#        raise "Please enter node#, proc#, phiname, aname, gxname and gyname!"
#        exit()
    
    t0 = time()
    if len(sys.argv) < 2:
        raise "Please enter core_total!"
        exit()
    elif len(sys.argv) == 2: #core_total only
        merge(sys.argv[1])
    elif len(sys.argv) == 3: #core_total, output_name
        merge(sys.argv[1], sys.argv[2])
    else: #core_total, output_name, a, gx, gy
        merge(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    t1 = time()
    print t1-t0
