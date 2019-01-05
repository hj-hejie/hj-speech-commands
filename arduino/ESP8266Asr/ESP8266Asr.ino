#include <ESP8266BaseService.h>

ESP8266BaseService bs;
WiFiClient client;
String str_payload;

void setup()
{
  bs.begin("hjwifi", "hejiepassw0rd", "ESP8266AsrRecord");
  if (!client.connect("hejie-ThinkPad-L450.local", 8009)) {
    Serial.println("Asr server connection failed");
  }
}

void loop()
{
  Serial.println("ESP8266AsrRecord recording........");
  for(int j=0; j<2; j++){
    for(int i=0;i<10000;i++)
    {
      str_payload += char(analogRead(A0)/4);
    }
    client.print(str_payload);
    str_payload="";
  }
  Serial.println("ESP8266AsrRecord recorded");
}
