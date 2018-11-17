#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

class ESP8266BaseService {

  private:
  
    MDNSResponder mdns;
    ESP8266WebServer http;

    String _dnsName;
    IPAddress _ip;
    String _wifi;

    typedef std::function<void(void)> THandlerFunction;
  
  public:
    ESP8266BaseService();
    void begin(char* dnsName);
    void begin(char* wifiSid, char* wifiPassword, char* dnsName);
    void httpon(const String &uri, THandlerFunction handler);
    void httpHandleClient();
};
