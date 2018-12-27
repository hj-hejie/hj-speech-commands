import pdb
import logging
import os
import sys
import time
import multiprocessing
from multiprocessing import Process, Queue, Pool
import paho.mqtt.client as mqtt
from homeassistant.const import EVENT_HOMEASSISTANT_START
sys.path.append(os.getcwd())
import hjtorch
import hjvad
import hjlog

LOG = logging.getLogger(__name__)

DOMAIN = 'pytorchasr'

N_PROC = 10

async def async_setup(hass, config):
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, pytorchasrstart)
    return True

class Mqttclient:
    def __init__(self, queues, topic = 'pytorchasr'):
        try:
            LOG.debug('Mqtt client %s start' % topic)
            self.topic = topic
            self.queues = queues
            self.l_queues = len(queues)
            self.i_queues = 0
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect('hejie-ThinkPad-L450.local', 1883, 60)
            self.client.loop_forever()
        except Exception as e:
            LOG.exception(e)

    def on_connect(self, client, userdata, flags, rc):
        try:
            LOG.debug("Topic %s Connected with result code %s"%(self.topic, str(rc)))
            client.subscribe(self.topic)
        except Exception as e:
            LOG.exception(e)
    
    def on_message(self, client, userdata, msg):
        try:
            LOG.debug('Mqtt channel %s put msg' % self.i_queues)
            self.queues[self.i_queues].put(msg.payload)
            self.i_queues = (self.i_queues + 1) % self.l_queues
        except Exception as e:
            LOG.exception(e)

def byte2frame(byte_queue, frame_queue):
    try:
        while True:
            byte = byte_queue.get()
            isspeech = hjvad.vad.is_speech(byte)
            frame = hjvad.Frame(byte, isspeech=isspeech)
            frame_queue.put(frame)
    except Exception as e:
        LOG.exception(e)

def pytorchasrstart():
    byte_queues = []
    frame_queues = []
    procs = []
    for i in range(N_PROC):
        byte_queues.append(Queue())
        frame_queues.append(Queue())
        procs.append(Process(target=byte2frame, args=(byte_queues[i], frame_queues[i])))
        procs[i].start()

    Process(target = Mqttclient, args = (byte_queues, )).start()

    pool = Pool(multiprocessing.cpu_count()-1)
    for segment in hjvad.vad_split(frame_queues, N_PROC):
        pool.apply_async(hjtorch.predict, args=(segment, ))  

if __name__ == '__main__':
    pytorchasrstart()
