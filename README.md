# Contactless Gesture-Controlled Robotic Gripper

A professional-grade, AI-driven robotic teleoperation system that enables zero-touch control of a mechanical gripper using real-time computer vision.

---

## 📸 Project Prototype
![Prototype](assets/prototypephysicalimage.jpeg)

---

## 🚀 Overview
The **Contactless Gesture-Controlled Robotic Gripper** is a hardware-agnostic control solution designed for sterile or hazardous environments. By replacing traditional joysticks with computer vision, users can manipulate a robotic arm by simply gesturing in front of a standard webcam.

### Key Features
* **AI Vision Processing:** Utilizes Google's MediaPipe framework to track 21 hand landmarks.
* **Low Latency:** Implements a high-speed WebSocket server to achieve <50ms response time.
* **Robust Architecture:** Features an isolated dual-power supply design to ensure stable logic communication even under heavy actuator loads.
* **Versatile Gripper:** Employs 3D-printed concentric gears for precise object manipulation.

---

## 🛠 Technical Stack
| Category | Technology |
| :--- | :--- |
| **Vision** | OpenCV, MediaPipe |
| **Microcontroller** | ESP32 NodeMCU |
| **Communication** | WebSocket (Asyncio) |
| **Hardware** | MG995 & SG90 Servos |

---

## ⚙️ Setup Instructions

### 1. Prerequisites
Ensure you have Python installed, then install the dependencies:
```bash
pip install opencv-python mediapipe websockets numpy

### 2. Running the Control Server
Navigate to the /src directory.
Locate mainserver.py and open it in any text editor.
Find the SERVER_IP variable and update it to your computer's local IP address (you can find this by typing ipconfig in CMD).
Start the server:
python src/mainserver.py

## 3. Firmware Upload (ESP32 Side)
Open the Arduino IDE.
Open the file firmware/esp32_mainserver/esp32_mainserver.ino.
In the code, locate the ssid and password variables and enter your Wi-Fi credentials.
Locate the server_ip variable in the Arduino code and set it to match the IP address you used in the Python script.
Select your ESP32 board and port in Tools > Board and Tools > Port.
Click Upload.

## 4. System Start-up Sequence

Power on the ESP32 (it will automatically connect to your Wi-Fi).
Launch the mainserver.py script on your laptop.
Once the server indicates "Connection Established," point your webcam at your hand to begin controlling the gripper.

## System Architecture

The system uses a client-server model where the laptop processes image data and broadcasts control commands via Wi-Fi.
Logic Circuit: Powered independently to maintain Wi-Fi stability.
Actuator Circuit: Powered by a high-amperage source to handle motor torque.
Grounding: Common ground configuration ensures seamless PWM signal transmission.

## 👨‍💻 Developer
* **Rohit Ahirwar**

---
*Built with passion for advanced robotics and sterile interaction.*
