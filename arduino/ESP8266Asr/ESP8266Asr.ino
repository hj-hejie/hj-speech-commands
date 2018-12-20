#include <ESP8266BaseService.h>

ESP8266BaseService bs;
WiFiClient client;
String str_payload;
char isok;

void setup()
{
  bs.begin("hjwifi", "hejiepassw0rd", "ESP8266Asr");
  if (!client.connect("hejie-ThinkPad-L450.local", 8009)) {
    Serial.println("connection failed");
  }	else{
    Serial.println("Asr server connected");
  }
}

void loop()
{
  isok = client.read();
  if(isok == '1'){
    Serial.println("ESP8266Asr sounding........");
    for(int i=0;i<10000*0.02;i++)
    {
      str_payload += char(analogRead(A0)/4);
    }
    client.print(str_payload);
    Serial.println("ESP8266Asr sounding ended");
    str_payload="";
    isok='';
  }
}
