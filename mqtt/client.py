import paho.mqtt.client as mqtt
import random

HOST = "hejie-ThinkPad-L450.local"
PORT = 1883

def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    for j in range(2):
        buf=[]
        for i in range(200):
            buf.append(random.randint(0,2**8-1))
        fms_byte=bytes(buf)
        client.publish('pytorchasr', fms_byte, 2)
    client.loop_forever()

if __name__ == '__main__':
    test()
