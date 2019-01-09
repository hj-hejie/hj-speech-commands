#!/usr/bin/python

import os
import shutil
import pdb
import contextlib
import wave
from pyaudio import PyAudio

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
                for j, file in enumerate(os.listdir(dir4)):
                    if j is 0:
                        for i in range(2000):
                            print(j, os.path.join(os.path.realpath(dir4), file)+'-->'+os.path.join(os.path.realpath(dir4), 's'+str(i)+file))
                            os.symlink(os.path.join(os.path.realpath(dir4), file), os.path.join(os.path.realpath(dir4), 's'+str(i)+file))

def builddataset():
    for classdir in set(os.listdir(dsdir))-set(['silence16hz', 'test']):
        classfulldir=os.path.join(dsdir, classdir)
        wavs=os.listdir(classfulldir)
        for i, wav in enumerate(wavs):
            wavfulldir=os.path.join(classfulldir, wav)
            if i%3 is 0 or classdir == '_background_noise_':
                totypefulldir=os.path.join(todsdir, 'train')
            elif i%3 is 1:
                totypefulldir=os.path.join(todsdir, 'test')
            else:
                totypefulldir=os.path.join(todsdir, 'valid')
            if not os.path.exists(totypefulldir):
               os.mkdir(totypefulldir) 
            tofulldir=os.path.join(totypefulldir, classdir)
            if not os.path.exists(tofulldir):
               os.mkdir(tofulldir) 
            towavfulldir=os.path.join(tofulldir, wav)
            print(wavfulldir,'->',towavfulldir)
            shutil.copyfile(wavfulldir,towavfulldir)

def buildvaddataset():
    for classdir in set(os.listdir(dsdir))-set(['silence16hz', 'test']):
        classfulldir=os.path.join(dsdir, classdir)
        wavs=os.listdir(classfulldir)
        for i, wav in enumerate(wavs):
            wavfulldir=os.path.join(classfulldir, wav)
            if i%3 is 0:
                totypefulldir=os.path.join(todsdir, 'train')
            elif i%3 is 1:
                totypefulldir=os.path.join(todsdir, 'test')
            else:
                totypefulldir=os.path.join(todsdir, 'valid')
            if not os.path.exists(totypefulldir):
               os.mkdir(totypefulldir)
            if classdir == '_background_noise_':
                tofulldir=os.path.join(totypefulldir, 'noise')
            else:
                tofulldir=os.path.join(totypefulldir, 'speech')
            if not os.path.exists(tofulldir):
               os.mkdir(tofulldir)
            for k, frame in enumerate(read_frames(wavfulldir)):
                towavfulldir=os.path.join(tofulldir, str(k)+'chunk'+wav)
                #write_wave(towavfulldir, frame)
                print(towavfulldir)
    #shutil.copytree(os.path.join(dsdir, '_background_noise_'), os.path.join(todsdir, 'train', '_background_noise_'))

def read_frames(path, duration_time=0.02, range_time=0.5):
    _range=int(10000*range_time)
    duration=int(10000*duration_time)
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        pcm_data = wf.readframes(wf.getnframes())
        if '_background_noise_' in path:
            pcm_data_ranged = pcm_data[_range:-_range]
        else:
            _input = input('%s range:' % path)
            while _input is not 's':
                _range = _input.split(',')
                pcm_data_ranged = pcm_data[int(_range[0]) : int(_range[0]) + 200 * int(_range[1])]
                play(pcm_data_ranged)
                _input = input('%s range:' % path)
        for i in range(0, len(pcm_data_ranged), duration):
            yield pcm_data_ranged[i: i+duration];


def write_wave(path, frames):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(1)
        wf.setframerate(10000)
        wf.writeframes(frames)

def read_frames_range():
    with contextlib.closing(wave.open('datasets/speech_commands_esp/kaideng/20190106150628.wav', 'rb')) as wf:
    #with contextlib.closing(wave.open('datasets/speech_commands_esp/guandeng/20181209192315.wav', 'rb')) as wf:
        pcm_data = wf.readframes(wf.getnframes())
        pcm_data_ranged = pcm_data[11000 : -1000]
        #write_wave('chunk03.wav', pcm_data_ranged)
        play(pcm_data_ranged)

def play(frames):
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(1),channels=1,rate=10000,output=True)
    stream.write(frames)
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__=='__main__':
    #builddataset()
    #createlinkdataset()
    buildvaddataset()
    #read_frames_range()
