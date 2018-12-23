import pdb
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("pytorchasr1")
    client.subscribe("pytorchasr2")

def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('hejie-ThinkPad-L450.local', 1883, 60)
client.loop_forever()
