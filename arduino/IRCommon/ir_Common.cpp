#include "ir_Common.h"
#include <algorithm>
#ifndef ARDUINO
#include <string>
#endif
#include "IRremoteESP8266.h"
#include "IRrecv.h"
#include "IRsend.h"
#include "IRutils.h"
#include "ir_Kelvinator.h"

IRCommonAC::IRCommonAC(uint16_t pin) : _irsend(pin) {
  gcString="";
}

void IRCommonAC::sendGCString(String str) {
  int16_t index;
  uint16_t count;

  // Find out how many items there are in the string.
  index = -1;
  count = 1;
  do {
    index = str.indexOf(',', index + 1);
    count++;
  } while (index != -1);

  // Now we know how many there are, allocate the memory to store them all.
  code_array = reinterpret_cast<uint16_t*>(malloc(count * sizeof(uint16_t)));
  // Check we malloc'ed successfully.
  if (code_array == NULL) {  // malloc failed, so give up.
    Serial.printf("\nCan't allocate %d bytes. (%d bytes free)\n",
                  count * sizeof(uint16_t), ESP.getFreeHeap());
    Serial.println("Giving up & forcing a reboot.");
    ESP.restart();  // Reboot.
    delay(500);  // Wait for the restart to happen.
    return;  // Should never get here, but just in case.
  }

  // Now convert the strings to integers and place them in code_array.
  count = 0;
  uint16_t start_from = 0;
  do {
    index = str.indexOf(',', start_from);
    code_array[count] = str.substring(start_from, index).toInt();
    start_from = index + 1;
    count++;
  } while (index != -1);

#if SEND_GLOBALCACHE
  _irsend.sendGC(code_array, count);  // All done. Send it.
#endif  // SEND_GLOBALCACHE
  free(code_array);  // Free up the memory allocated.
}

void IRCommonAC::begin() {
  _irsend.begin();
}

void IRCommonAC::send() {
 sendGCString(gcString); 
}

void IRCommonAC::on() {
}

void IRCommonAC::off() {
}

#endif
