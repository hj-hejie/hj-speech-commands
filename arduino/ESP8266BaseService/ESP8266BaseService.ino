#include <ESP8266BaseService.h>

ESP8266BaseService bs;

void setup(){
  bs.begin("esp8266");
  bs.http.on("/hejie",[](){
    bs.http.send(200, "application/json","{\"name\":\"hejie\"}");
  });
}

void loop(){
  bs.http.handleClient();
}
