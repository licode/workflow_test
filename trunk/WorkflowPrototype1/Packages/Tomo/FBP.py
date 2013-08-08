#! usr/bin/env python
"""
    Filtered backprojection from phantom image
    example:
    $> python FBP.py "output.tif" 0 180 1
"""
import sys
import numpy as np
import matplotlib.pyplot as pl
import Image
import phantom
import parallel_beam as pb
from workflow.workflow_setting import home_path, result_path

display_flag = False

def recon(projections, a_min = 0, a_max = 180, a_inc = 1):
    angle = np.arange (a_min, a_max, a_inc)
    reconstruction = pb.iradon (projections, angle)
    reconstruction = 255*(reconstruction-reconstruction.min())/(reconstruction.max()-reconstruction.min())
    return reconstruction

if __name__ == '__main__':
    filename = ''
    a_min = 0
    a_max = 180
    a_inc = 1
  
    if len(sys.argv) < 5:
        print len(sys.argv)
        print 'use default settings'
    else:
        filename = str(sys.argv[1])
        a_min = float(sys.argv[2])
        a_max = float(sys.argv[3])
        a_inc = float(sys.argv[4])
    oname = home_path+'Data/Tomo/projs/projections_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.npy'
    projs = np.load(oname)

    if display_flag:
        pl.ion()
        pl.figure(1)
        pl.subplot(121)
        pl.xlabel('Sinogram')
        pl.imshow(projs, cmap = pl.cm.gray)
        pl.draw()
        pl.ioff()

    reconstruction = recon(projs, a_min, a_max, a_inc)
    im = Image.fromarray(np.uint8(reconstruction))
    im.save(result_path+filename)

    if display_flag:
        pl.ion()
        pl.figure(1)
        pl.subplot(122)
        pl.xlabel('Reconstructed Result')
        pl.imshow(im, cmap = pl.cm.gray)
        pl.draw()
        pl.ioff()
        pl.show()
