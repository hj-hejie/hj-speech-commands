#include "ESP8266BaseService.h"

ESP8266BaseService::ESP8266BaseService():http(80){
}

void ESP8266BaseService::begin(char* dnsName){
  begin("19KFS", "abcd1234", dnsName);
}

void ESP8266BaseService::begin(char* wifiSid, char* wifiPassword, char* dnsName){
  _dnsName=dnsName;
  _wifi=wifiSid;
  
  Serial.begin(115200);
  delay(100);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifiSid, wifiPassword);
  Serial.print("Connecting tos ");
  Serial.println(wifiSid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  _ip=WiFi.localIP();
  Serial.print("\nWiFi Connected:");
  Serial.println(_ip);

  if (!MDNS.begin(dnsName)) {
    Serial.println("Error setting up MDNS responder!");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("MDNS responder started");

  http.on("/", [this](){
    http.send(200, "text/html",
            "<html>" \
              "<head><title>"+_dnsName+"</title></head>" \
              "<body>" \
                "<div>ip:"+_ip+"</div>"\
                "<div>wifi:"+_wifi+"</div>"\
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
