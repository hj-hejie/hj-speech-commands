#ifndef IR_COMMON_H_
#define IR_COMMON_H_

#define __STDC_LIMIT_MACROS
#include <stdint.h>
#ifndef UNIT_TEST
#include <Arduino.h>
#else
#include <string>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"

// Classes
class IRCommonAC {
 public:
  explicit IRGreeAC(uint16_t pin);
  void send();
  void begin();
  void on();
  void off();

 private:
  void sendGCString(String str);
  IRsend _irsend;
  String gcString;
};

#endif
