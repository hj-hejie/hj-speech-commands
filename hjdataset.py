#!/usr/bin/python

import os
import shutil

dsdir='datasets/speech_commands_esp/'

todsdir='datasets/speech_commands/'
if not os.path.exists(todsdir):os.mkdir(todsdir)

totraindir=todsdir+'train/'
if not os.path.exists(totraindir):os.mkdir(totraindir)
tonoisedir=totraindir+'_background_noise_/'

totestdir=todsdir+'test/'
if not os.path.exists(totestdir):os.mkdir(totestdir)

tovaliddir=todsdir+'valid/'
if not os.path.exists(tovaliddir):os.mkdir(tovaliddir)

def copylimitdataset():
    dirs=os.listdir(dsdir)
    for dir in dirs:
        dsdirdir=os.path.join(dsdir, dir)
        if os.path.isdir(dsdirdir):
            for subdir in os.listdir(dsdirdir):
                dsdirdirsubdir=os.path.join(dsdirdir, subdir)
                if os.path.isdir(dsdirdirsubdir):
                    if subdir=='_background_noise_':
                        if os.path.exists(tonoisedir):
                            shutil.rmtree(tonoisedir)
                        shutil.copytree(dsdirdirsubdir, tonoisedir)
                    else:
                        topath=os.path.join(todsdir, dir, subdir)
                        if not os.path.exists(topath): os.mkdir(topath)
                        for wav in os.listdir(dsdirdirsubdir)[0:5]:
                            wavpath=os.path.join(dsdirdirsubdir, wav)
                            towavpath=os.path.join(topath, wav)
                            shutil.copyfile(wavpath, towavpath)

def createlinkdataset():
    for dir in os.listdir(todsdir):
        dir2=os.path.join(todsdir, dir)
        for dir3 in os.listdir(dir2):
            dir4=os.path.join(dir2, dir3)
            if dir3 != '_background_noise_':
                for file in os.listdir(dir4):
                    for i in range(2000):
                        print(os.path.join('.', file)+'-->'+os.path.join(dir4, 's'+str(i)+file))
                        os.symlink(os.path.join('.', file), os.path.join(dir4, 's'+str(i)+file))

def builddataset():
    for classdir in set(os.listdir(dsdir))-set(['silence16hz', 'test']):
        print('%s'%classdir)
        

if __name__=='__main__':
    builddataset()
