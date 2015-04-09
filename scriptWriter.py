#! /usr/local/bin/anaconda/bin/python

import numpy as np
import os,sys,fnmatch
mClustPath = os.getcwd()+'/MClust-4.3'
##########################FUNCTIONS

def locate(pattern, root=os.curdir):
    '''
    Locate all files matching supplied filename pattern in and below
        supplied root directory.
    Parameters
    ----------
        pattern : string
            A string representing pattern you want to look for in the path.
        root : string
            contains the path address you want to look trough!
    Returns
    ----------
        Array of strings consist of two column, first contains the path and second the file names that matched 
        the desired pattern.
    '''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield [path,filename]
            
def mmap_ntt_file(filename):
    """ Memory map the Neuralynx .ntt file """ 
    ntt_dtype = np.dtype([
        ('timestamp'  , '<u8'),
        ('sc_number'  , '<u4'),
        ('cell_number', '<u4'),
        ('params'     , '<u4',   (8,)),
        ('waveforms'  , '<i2', (32,4)),
    ])
    return np.memmap(filename, dtype=ntt_dtype, mode='readwrite',
       offset=(16 * 2**10)) 

def ChannelValidity(fileName):
    """
    A function to examine the data from different channels of a tetrode stored in Neuralynx ntt file.
    """ 
    ntt = mmap_ntt_file(fileName)
    RndIdx = np.random.randint(ntt.size-1,size=100)
    sample = np.array(ntt['waveforms'][RndIdx])
    chV = np.array([])
    ChannelValidity = np.array([])
    for item in sample:
        chV = np.append(chV,np.array([item[:,ii].sum() for ii in range(4)]))
    chV = chV.reshape(chV.size/4,4)
    ChannelValidity = np.append(ChannelValidity,[chV[:,jj].sum() for jj in range(4)])
    for ii in range(4):
        if ChannelValidity[ii] > 10:
            ChannelValidity[ii] = 1
        else:
            ChannelValidity[ii] = 0
    return np.int0(ChannelValidity)

#########################################################
if len(sys.argv) > 1:
    try: 
        path = sys.argv[1]
    except:
        print "Usage:", sys.argv[0], "path_to_data"; sys.exit(1)

with open(path+'mScripts/features.sh','w') as bashfile:
    bashfile.write("#!/bin/bash\n")
    bashfile.write("matlab -nodesktop << EOF  \n")
    bashfile.write("cd (\'%s\') \n" %path)
    bashfile.write("addpath(genpath(\'%s\')) \n" %mClustPath)
    for item in locate('*.ntt',path):
        chV = ChannelValidity(os.path.join(item[0],item[1]))
        if chV.sum > 1 and item[0] == path[:-1]:
              bashfile.write("RunClustBatch(\'fcTT\',{\'%s\'},\'channelValidity\', %s) \nResetMClust\n"
                          %(item[1],chV))
    bashfile.write('wait \n')
    bashfile.write('exit; \nEOF\n')
    bashfile.write('echo Feature files have been successfully written!!! \n')
print 'bash script for running MClust is written to ./mScripts folder!!!'

