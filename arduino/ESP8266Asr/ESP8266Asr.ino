 #include <ESP8266BaseService.h>
 #include <PubSubClient.h>

ESP8266BaseService bs;
WiFiClient client;
PubSubClient mqttclient(client);
const int len_payload = 10000*2;

void reconnect() {
  // Loop until we're reconnected
  while (!mqttclient.connected()) {
    Serial.println("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (mqttclient.connect(clientId.c_str())) {
      Serial.println("mqtt connected");
    } else {
      Serial.print("mqtt connect failed, rc=");
      Serial.print(mqttclient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup()
{
  bs.begin("hjwifi", "hejiepassw0rd", "ESP8266Asr");
  mqttclient.setServer("hejie-ThinkPad-L450.local", 1883);
}

void loop()
{
  if (!mqttclient.connected()) {
    reconnect();
  }
  mqttclient.loop();
  
  mqttclient.beginPublish("pytorchasr1", len_payload, false);
  Serial.println("ESP8266Asr sounding........");
  for(int i = 0; i < len_payload; i++)
  {
    mqttclient.print(char(analogRead(A0)/4));
  }
  mqttclient.endPublish();
  Serial.println("ESP8266Asr sounding ended");
}
