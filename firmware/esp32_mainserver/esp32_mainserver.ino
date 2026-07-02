#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ESP32Servo.h>

// --- Wi-Fi & Server Settings ---
const char* ssid = "YOUR WIFI NAME";
const char* password = "YOUR WIFI PASSWARD";
const char* server_ip = "YOUR IP ADDRESS IPv4"; 
const uint16_t server_port = 8765;

WebSocketsClient webSocket;

Servo wristPanServo;  
Servo wristTiltServo; 
Servo gripperServo; 

// --- Your Exact Pins ---
const int panPin = 13;     // Base Left/Right
const int tiltPin = 12;    // Arm Up/Down
const int gripperPin = 14; // Gripper Open/Close

void setup() {
  Serial.begin(115200);

  // ESP32 requires a timer for every servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);

  // Attach servos to pins
  wristPanServo.attach(panPin);
  wristTiltServo.attach(tiltPin);
  gripperServo.attach(gripperPin);

  // Set initial starting positions
  wristPanServo.write(90);  
  wristTiltServo.write(90); 
  gripperServo.write(90); // Start with gripper wide open

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");

  webSocket.begin(server_ip, server_port, "/");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop(); 
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String msg = (char*)payload;
    
    int p_val, t_val, g_val;
    
    // Now extracting P (Pan), T (Tilt), AND G (Gripper)
    if (sscanf(msg.c_str(), "P:%d,T:%d,G:%d", &p_val, &t_val, &g_val) == 3) {
      
      // Instantly move all three servos
      wristPanServo.write(p_val);
      wristTiltServo.write(t_val);
      gripperServo.write(g_val);
      
    }
  }
}