#include <ESP8266BaseService.h>

ESP8266BaseService bs;
WiFiClient client;

void setup(){
  if (!client.connect("hejie-ThinkPad-L450.local", 8009)) {
    Serial.println("connection failed");
  }
}

void loop(){
  client.print("hejie");
}
