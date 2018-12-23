import paho.mqtt.client as mqtt

HOST = "hejie-ThinkPad-L450.local"
PORT = 1883

def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    client.publish("pytorchasr1","hello chenfulin",2)
    client.publish("pytorchasr2","hello chenfulin",2)
    client.loop_forever()

if __name__ == '__main__':
    test()
