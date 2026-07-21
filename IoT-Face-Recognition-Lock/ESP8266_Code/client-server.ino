#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
unsigned long int unlockTime = 0;
bool unlock  = false;
const uint16_t port = 1250;
const char *host = "192.168.43.17";
WiFiClient client;
void setup()
{
  Serial.begin(115200);
  Serial.println("Connecting...\n");
  WiFi.mode(WIFI_STA);
  WiFi.begin("hd", "123456hossein"); // change it to your ussid and password
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);
}

void loop()
{
  if (!client.connect(host, port))
  {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }
  Serial.println("Connected to server successful!");
  while (1) {
    if (unlock && (millis () - unlockTime >= 2000)) {
      Serial.println( "Closein Door");
      digitalWrite(14,HIGH );
      unlock = false;
    }
    String bufffer = "";
    while (client.available() > 0)
    {
      char c = client.read();
      if ( c == 'M') {
        Serial.println(bufffer);
        if (bufffer == "OPEN") {
          Serial.println( "Openin Door");
          unlockTime = millis ();
          digitalWrite(14, LOW);
          unlock = true;
        }
      } else {
        bufffer.concat(c);
      }
    }
  }
  client.stop();
  delay(5000);
}
