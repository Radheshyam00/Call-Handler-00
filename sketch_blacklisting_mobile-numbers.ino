#include <SoftwareSerial.h>

SoftwareSerial sim900(7, 8);  // SIM900 TX → Pin 7, RX → Pin 8

// List of blocked numbers
String blockedNumbers[] = {"+917379915439", "+918824043348"};  
int blockedCount = 2;

void setup() {
  Serial.begin(9600);
  sim900.begin(9600);

  Serial.println("SIM900A Call Blocker Initialized...");

  // Enable caller ID notification
  sim900.println("AT+CLIP=1");
  delay(1000);
}

void loop() {
  if (sim900.available()) {
    String callData = sim900.readString();
    Serial.println(callData);

    if (callData.indexOf("RING") != -1) { 
      Serial.println("Incoming Call...");
      delay(1000);

      sim900.println("AT+CLCC");  // Get active call details
      delay(1000);

      if (sim900.available()) {
        String callerID = sim900.readString();
        Serial.println("Caller Info: " + callerID);

        for (int i = 0; i < blockedCount; i++) {
          if (callerID.indexOf(blockedNumbers[i]) != -1) {
            Serial.println("Blocked Number Detected! Hanging up...");
            sim900.println("ATH");  // Hang up call
            break;
          }
        }
      }
    }
  }
}
