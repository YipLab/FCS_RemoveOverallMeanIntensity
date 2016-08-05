####from PIL import Image
####import time
##from subprocess import call
##import tifffile
##from scipy import stats
##from scipy import ndimage


import sys
import os
import numpy as np
import glob
import javabridge as jv
import bioformats as bf
jv.start_vm(class_path=bf.JARS)
import matplotlib.pyplot as pp

os.chdir(sys.argv[1])
FileName=glob.glob('*.tif')##test3_quantem_1ms_emg1000_lp_high_1_MMStack.ome.tif

for katN in FileName:
    print(katN)
    rdr = bf.ImageReader(katN, perform_init=True)
    FileNameOut='MeanSubs_'+FileName[0]
    Meta = bf.get_omexml_metadata(FileName[0])
    md = bf.omexml.OMEXML(Meta)
    pixels = md.image().Pixels
    ImgNums=pixels.SizeT
    img = rdr.read(t=0,rescale=False)
    SaveImg=np.zeros([pixels.SizeY,pixels.SizeX,min(ImgNums,45000)])
    #bf.write_image(FileNameOut,img,'uint16',c=0,z=0,t=0,size_c=1,size_z=1,size_t=ImgNums,channel_names=None)
    SaveImg[:,:,0]=img
    ImgKeepMean = img.mean()
    for kat in np.arange(1,min(ImgNums,45000)):##ImgNums):
        img = rdr.read(t=kat,rescale=False)
        ICorr=ImgKeepMean-img.mean()
        ImgMeanCorr = img+ICorr
        SaveImg[:,:,kat]=ImgMeanCorr
        ##print('Image '+str(kat)+' done!')
    bf.write_image(FileNameOut,SaveImg,'uint16')
    
print('All done!')
