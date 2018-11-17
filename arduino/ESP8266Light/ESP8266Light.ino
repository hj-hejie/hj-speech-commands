#include <ESP8266BaseService.h>

ESP8266BaseService bs;

void setup(){
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  
  bs.begin("esp8266light");
  
  bs.http.on("/on",[](){
    digitalWrite(LED_BUILTIN, LOW);
    ok();
  });
  
  bs.http.on("/off",[](){
    digitalWrite(LED_BUILTIN, HIGH);
    ok();
  });
}

void loop(){
  bs.http.handleClient();
}

void ok(){
  bs.http.send(200, "application/json","{\"success\":1}");
}
