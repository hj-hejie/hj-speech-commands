#!/usr/bin/python

import serial
from time import sleep
import json
import os

if __name__ == '__main__':
    keys={}
    filename='irrawcode_tv.json'

    if os.path.exists(filename):
        with open(filename) as f:
            keys=json.load(f)
    serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5) 
    if serial.isOpen() :
        print('open success')
    else :
        print('open failed')

    try:
        while True :
            data = serial.readline()
            if data != b'':
                datastr=data.decode()
                if datastr.startswith('uint16_t rawData'):
                    rawcode=datastr[ datastr.index('{')+1: datastr.index('}')-1 ].replace(' ','')
                    print('ir raw code : ', rawcode)
                    key=input('input key name>')
                    keys[key]=rawcode
                else:
                    sleep(0.02)
            else:
                sleep(0.02)

    except KeyboardInterrupt:
        with open(filename, 'w') as f:
            json.dump(keys, f)
