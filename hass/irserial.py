import serial
from time import sleep
import json
import os

if __name__ == '__main__':
    keys={}
    filename='irrawcode.txt'
    if os.path.exists(filename):
        with open(filename) as f:
            keys=json.load(f)
    serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5) 
    if serial.isOpen() :
        print('open success')
    else :
        print('open failed')

    try:
        while(True):
            data = serial.read_all()
            if data != '':
                print('ir raw code : ',data)
                key=input('input key name>')
                keys[key]=data
            else:
                sleep(0.02)

    except KeyboardInterrupt:
        with open(filename, 'w') as f:
            json.dump(keys, f)
