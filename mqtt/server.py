import pdb
import sys
import paho.mqtt.client as mqtt
import time
from multiprocessing import Pool
import multiprocessing
from logging import INFO
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': 'hjlog.txt',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': INFO,
        },
    }
})

import logging
logger = logging.getLogger(__name__)

class Mqttclient:
    def __init__(self, topic):
        try:
            self.topic = topic
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect('hejie-ThinkPad-L450.local', 1883, 60)
            self.client.loop_forever()
        except Exception as e:
            logger.exception(e)
    
    def on_connect(self, client, userdata, flags, rc):
        try:
            logger.info("Topic %s connected with result code %s\n"%(self.topic, str(rc)))
            client.subscribe(self.topic)
        except Exception as e:
            logger.exception(e)
    
    def on_message(self, client, userdata, msg):
        try:
            logger.info(msg.topic+" " + ":" + str(msg.payload) + "\n")
            time.sleep(10)
            logger.info(msg.topic+" done\n")
        except Exception as e:
            logger.exception(e)

if __name__ == '__main__':
    try:
        logger.info('start')
        #pool=Pool(multiprocessing.cpu_count()-1)
        pool=Pool(200)
        for i in range(200):
            pool.apply_async(Mqttclient, args=('hejie%s'%i, ))
        pool.close()
        pool.join()
    except Exception as e:
        logger.exception(e)
