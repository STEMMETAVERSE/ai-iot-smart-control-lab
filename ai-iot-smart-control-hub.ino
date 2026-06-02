#include <WiFiS3.h>
char ssid[] = "YOUR_WIFI";
char pass[] = "YOUR_PASS";
WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    String command = client.readStringUntil('\n');

    if (command == "LED_ON") {
      digitalWrite(13, HIGH);
    }

    if (command == "LED_OFF") {
      digitalWrite(13, LOW);
    }
  }
}

