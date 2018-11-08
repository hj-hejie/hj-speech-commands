#include "ESP8266BaseService.h"

ESP8266BaseService::ESP8266BaseService(char* dnsName){
  ESP8266BaseService("", "", dnsName);
}

ESP8266BaseService::ESP8266BaseService(String wifiSid, String wifiPassword, char* dnsName):http(80){
  
  WiFi.begin("", "");
  Serial.println("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nWiFi Connected");

  if (mdns.begin(dnsName, WiFi.localIP())) {
    Serial.println("MDNS responder started");
  }

  http.on("/", [this](){
    http.send(200, "text/html",
            "<html>" \
              "<head><title>hejie</title></head>" \
              "<body>" \
                "<h1>hejie</h1>" \
              "</body>" \
            "</html>");
  });
  http.onNotFound([this](){
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += http.uri();
    message += "\nMethod: ";
    message += (http.method() == HTTP_GET)?"GET":"POST";
    message += "\nArguments: ";
    message += http.args();
    message += "\n";
    for (uint8_t i = 0; i < http.args(); i++)
      message += " " + http.argName(i) + ": " + http.arg(i) + "\n";
    http.send(404, "text/plain", message);
  });
  http.begin();
  Serial.println("HTTP server started");
}

void ESP8266BaseService::httpon(const String &uri, THandlerFunction handler){
  http.on(uri, handler);
}

void ESP8266BaseService::httpHandleClient(){
  http.handleClient();
}
