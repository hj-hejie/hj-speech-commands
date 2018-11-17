#include "ESP8266BaseService.h"

ESP8266BaseService bs;

void setup(){
  bs.httpon("/hejie", [](){});
}
void loop(){
  bs.httpHandleClient();
}
