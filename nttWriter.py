#! /usr/local/bin/anaconda/bin/python

'''
Created on Apr 07, 2015

@author: chenani
'''
###############MODULES
import os,sys
import numpy as np
from genericpath import isfile
import fnmatch

###############FUNCTIONS
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


if len(sys.argv) > 1:
    try: 
        path = sys.argv[1]
    except:
        print "Usage:", sys.argv[0], "path_to_data"; sys.exit(1)


cluList = []
if os.path.isdir(path):
    #nttList = [ item for item in trees.locate('*.ntt', path)]          
    cluList = [item for item in locate('*.clu.*', path)]
    cluList = [item for item in cluList if item[1].find('.temp.') < 1]
    if len(cluList):
        print 'Loding Files...'
    else:
        print 'No .clu file found... Plese cluster your data using KlastaKwik first...'   

for item in cluList:
    print item

for item in cluList:
    fileBase = item[1].split('.')[0]
    cluFile = os.path.join(item[0],item[1])
    cll = np.loadtxt(cluFile)
    cll = np.uint32(cll)
    if item[0].endswith('FD'):
        nttFile = os.path.join(item[0][:-2],fileBase+'.ntt')
        nttsFile = os.path.join(item[0][:-2],fileBase+'ss.ntt')
    else:
        nttFile = os.path.join(item[0],fileBase+'.ntt')
        nttsFile = os.path.join(item[0],fileBase+'ss.ntt')
    if isfile(nttFile):
        
        try:
            print 'Loading %s \n' %nttFile
            ntt = mmap_ntt_file(nttFile)
            nttLoaded = True
            pass
        except:
            print 'Could not load %s. \n Jumping to next file.' %nttFile
            nttLoaded = False
        if nttLoaded and cll.size - ntt.size ==1:
                for ii,item in enumerate(ntt['cell_number']):
                    ntt['cell_number'][ii] = cll[ii+1]
                ##################WRITE
                print 'Writing %s ...' %(nttFile)
                #ntt.tofile(nttsFile)
        else:
            print'Please check selected files. It seems there is a mismatch!'
    else:
        print 'file %s is missing!!!' %nttFile
             


