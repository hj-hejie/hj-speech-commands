#ifndef IR_COMMON_H_
#define IR_COMMON_H_
#endif
#include"FS.h"
#include "IRremoteESP8266.h"
#include "IRsend.h"
#include <ArduinoJson.h>

// Classes
class IRCommonAC {
 public:
  explicit IRCommonAC(uint16_t pin);
  void send();
  void begin();
  void on();
  void off();

 private:
  void sendGCString(String str);
  IRsend _irsend;
  String gcString="";
  String jsonFile="irrawcode_ac.json";
  JsonObject json;
  uint16_t *code_array;
};
