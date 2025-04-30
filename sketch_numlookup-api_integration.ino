#include <SoftwareSerial.h>

SoftwareSerial sim900(7, 8); // SIM900 TX → Pin 7, RX → Pin 8
String serverURL = "https://129zk4mn9b.execute-api.ap-southeast-2.amazonaws.com/prod/senddata"; // Replace with API Gateway URL

void setup() {
  Serial.begin(9600);
  sim900.begin(9600);

  Serial.println("Initializing...");
  sim900.println("AT+CLIP=1"); // Enable caller ID
  delay(1000);
}

void loop() {
  if (sim900.available()) {
    String callData = sim900.readString();
    Serial.println(callData);

    if (callData.indexOf("RING") != -1) {
      Serial.println("Incoming Call...");
      delay(1000);

      sim900.println("AT+CLCC"); // Get caller ID
      delay(1000);

      if (sim900.available()) {
        String callerID = sim900.readString();
        Serial.println("Caller: " + callerID);

        // Extract phone number
        int startIndex = callerID.indexOf("+");
        int endIndex = callerID.indexOf("\"", startIndex);
        if (startIndex != -1 && endIndex != -1) {
          String phoneNumber = callerID.substring(startIndex, endIndex);
          Serial.println("Checking Number: " + phoneNumber);

          // Send POST request to AWS Lambda
          sim900.println("AT+HTTPINIT");
          delay(1000);
          sim900.println("AT+HTTPPARA=\"CID\",1");
          delay(500);
          sim900.println("AT+HTTPPARA=\"URL\",\"" + serverURL + "\"");
          delay(1000);
          sim900.println("AT+HTTPPARA=\"CONTENT\",\"application/json\"");
          delay(500);

          // JSON Payload
          String jsonData = "{\"number\":\"" + phoneNumber + "\"}";
          int jsonLength = jsonData.length();

          // Send POST Request
          sim900.println("AT+HTTPDATA=" + String(jsonLength) + ",10000");
          delay(500);
          sim900.println(jsonData);
          delay(500);
          sim900.println("AT+HTTPACTION=1");
          delay(5000);
          sim900.println("AT+HTTPREAD");
          delay(2000);

          // Read response
          if (sim900.available()) {
            String response = sim900.readString();
            Serial.println("Server Response: " + response);

            if (response.indexOf("\"spam\":\"Yes\"") != -1) {
              Serial.println("SPAM Detected! Hanging up...");
              sim900.println("ATH");  // Hang up
            }
          }

          sim900.println("AT+HTTPTERM"); // End HTTP session
        }
      }
    }
  }
}
