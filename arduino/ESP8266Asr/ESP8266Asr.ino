#include <ESP8266BaseService.h>

ESP8266BaseService bs;
WiFiClient client;
String str_payload;
bool first=true;

void setup()
{
  bs.begin("ESP8266Asr");
  if (!client.connect("hejie-ThinkPad-L450.local", 8009)) {
    Serial.println("connection failed");
  }	
}

void loop()
{
  if(first){
    Serial.println("ESP8266Asr sounding***************");
    for(int i=0;i<20000;i++)
    {
      str_payload += char(analogRead(A0)/4);
    }
    client.print(str_payload);
    str_payload="";
    first=false;
  }
}
