#!/usr/bin/python

import os
import shutil

dsdir='datasets/speech_commands/'

todsdir='datasets/speech_commands2/'
if not os.path.exists(todsdir):os.mkdir(todsdir)

totraindir=todsdir+'train/'
if not os.path.exists(totraindir):os.mkdir(totraindir)
tonoisedir=totraindir+'_background_noise_/'

totestdir=todsdir+'test/'
if not os.path.exists(totestdir):os.mkdir(totestdir)

tovaliddir=todsdir+'valid/'
if not os.path.exists(tovaliddir):os.mkdir(tovaliddir)

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
					
