import pdb
import logging
import os
import sys
import time
import paho.mqtt.client as mqtt
from homeassistant.const import EVENT_HOMEASSISTANT_START
sys.path.append(os.getcwd())
import hjtorch
import hjvad

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'pytorchasr'

async def async_setup(hass, config):
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, pytorchasrstart)
    return True

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('pytorchasr1')
    client.subscribe('pytorchasr2')

#count=0

def on_message(client, userdata, msg):
    try:
        #global count
        #count+=1
        print(msg.topic+" " + ":" + str(len(msg.payload)))
        #hjvad.write_wave('hjtest%s.wav'%count, msg.payload)
        for i, segment in enumerate(hjvad.vad_split(msg.payload)):
            hjtorch.predict(segment)
    except Exception as e:
        logging.exception(e)
        

def pytorchasrstart():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('hejie-ThinkPad-L450.local', 1883, 60)
    client.loop_forever()

if __name__ == '__main__':
    pytorchasrstart()
